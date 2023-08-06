from typing import List, Dict, Optional
import pandas as pd
import numpy as np
import datetime
import traceback
import json
from functools import partial
import math
from sklearn.metrics import r2_score
import statsmodels.api as sm
import concurrent.futures
from sklearn.linear_model import LinearRegression
from scipy.optimize import Bounds, minimize
from statsmodels.tsa.ar_model import AutoReg, ar_select_order
from ...manager.manager_fund import FundDataManager
from ...manager.score import FundScoreManager
from ...wrapper.mysql import DerivedDatabaseConnector
from ...api.basic import BasicDataApi

class FundIndicatorProcessorGroup(object):

    _TRADING_DAYS_PER_YEAR = 242
    _NATURAL_DAYS_PER_YEAR = 365
    _RISK_FEE_RATE = 0.025
    _RISK_FEE_RATE_PER_DAY = _RISK_FEE_RATE / _TRADING_DAYS_PER_YEAR

    def __init__(self, data_helper):
        self._data_helper = data_helper
        self._basic_api = BasicDataApi()

    def init(self, start_date='20200809', end_date='20200809'):    
        self.log = []
        start_date: str = (pd.to_datetime(start_date) - datetime.timedelta(days=self._NATURAL_DAYS_PER_YEAR*2+1)).strftime('%Y%m%d')
        # 获取区间内交易日列表
        all_trading_days: pd.Series = self._basic_api.get_trading_day_list().drop(columns='_update_time').set_index('datetime')
        self._trading_days: pd.Series = all_trading_days.loc[pd.to_datetime(start_date).date():pd.to_datetime(end_date).date()]
        self.end_date = self._trading_days.index.values[-1]

        # 基金净值数据、指数价格数据的index对齐到交易日列表
        fund_nav: pd.DataFrame = self._basic_api.get_fund_nav_with_date(start_date, end_date)#, fund_list = f_l)
        self._fund_nav: pd.DataFrame = fund_nav.pivot_table(index='datetime', columns='fund_id', values='adjusted_net_value').reindex(self._trading_days.index).fillna(method='ffill')
        # 选取成立满半年的
        res = []
        for fund_id in self._fund_nav:
            if self._fund_nav[fund_id].dropna().shape[0] > 120:
                res.append(fund_id)
        self._fund_nav = self._fund_nav[res].copy()

        index_price: pd.DataFrame = self._basic_api.get_index_price_dt(start_date, end_date).drop(columns='_update_time')
        # 有的index最近没有数据，如活期存款利率/各种定期存款利率等，需要先reindex到全部的交易日列表上ffill
        self._index_price = index_price.pivot_table(index='datetime', columns='index_id', values='close').reindex(self._trading_days.index)#.fillna(method='ffill')
        _bank_rate_df = self._basic_api.get_index_price(index_list =['ddir', 'nonor', 'tmd_1y', 'tmd_2y', 'tmd_3m', 'tmd_3y', 'tmd_5y', 'tmd_6m', 'tmd_7d']).drop(columns='_update_time')
        _bank_rate_df = _bank_rate_df.pivot_table(index='datetime', columns='index_id', values='close').reindex(all_trading_days.index).fillna(method='ffill').reindex(self._trading_days.index)
        self._index_price = pd.concat([self._index_price, _bank_rate_df], axis=1)
        # 再reindex到参与计算的交易日列表上
        #self._index_price: pd.DataFrame = index_price.reindex(self._trading_days.index)
        pd.testing.assert_index_equal(self._fund_nav.index, self._index_price.index)
        try:
            # 这个指数有一天的点数是0，特殊处理一下
            self._index_price['spi_spa'] = self._index_price['spi_spa'].where(self._index_price.spi_spa != 0).fillna(method='ffill')
        except KeyError:
            pass

        # 对数净值取差分并且去掉第一个空值，得到基金对数收益率数列
        self._fund_ret: pd.DataFrame = np.log(self._fund_nav).diff().iloc[1:, :]

        self._fund_size = self._basic_api.get_fund_size_range(start_date, end_date)
        self._fund_size = self._fund_size.pivot_table(index='datetime', columns='fund_id', values='size').reindex(self._fund_ret.index).fillna(method='ffill')
        
        # 计算benchmark return，且index对齐到fund_ret
        benchmark_ret: pd.DataFrame = self._get_benchmark_return()
        self._benchmark_ret: pd.DataFrame = benchmark_ret.reindex(self._fund_ret.index)
        pd.testing.assert_index_equal(self._fund_ret.index, self._benchmark_ret.index)

        # 获取待计算的基金列表
        fund_list: pd.DataFrame = self._basic_api.get_fund_info().drop(columns='_update_time')
        self._fund_list: pd.DataFrame = fund_list[fund_list.structure_type <= 1]
        # 获取wind一级分类
        self._wind_class_1: np.ndarray = fund_list.wind_class_1.unique()
        self.get_continue_stats_tool()

    def df_resample(self, df):
        df.index = pd.to_datetime(df.index)
        df = df.resample('1W').sum()
        df.index = pd.Series(df.index).dt.date
        return df

    def stutzer_index(self, ex_return):
        ex_return = np.array(ex_return)
        information_statistic = lambda theta: np.log(np.mean(np.exp(theta[0] * ex_return)))
        theta0 = [-1.]
        bounds = Bounds((-np.inf), (100))
        result = minimize(information_statistic, theta0, method='SLSQP', bounds=bounds, tol=1e-16)
        if result.success:
            information_statistic = -result.fun
            stutzer_index = np.abs(np.mean(ex_return)) / np.mean(ex_return) * np.sqrt(2 * information_statistic)
            result = {'information_statistic': information_statistic,
                    'stutzer_index': stutzer_index,
                    'theta': result.x[0]}
        else:
            result = {'information_statistic': information_statistic,
                    'stutzer_index': np.nan,
                    'theta': result.x[0]}
            #print('未找到Information Statistic最大值')
            return result
        return result

    def _lambda_cl(self, x: pd.Series, fund_ret: pd.DataFrame):
        fund_id = x.name
        total = pd.concat({'Y': fund_ret[fund_id], 'x': x}, axis=1)
        total = total[total.notna().all(axis=1)]
        if total.empty:
            return {'beta':np.nan,
                    'alpha':np.nan,
                    'alpha_t':np.nan,
                    'alpha_p':np.nan,
                    'beta_t':np.nan,
                    'beta_p':np.nan,
                    }
        Y: pd.Series = total['Y']
        x = total['x']
        if x.count() != Y.count():
            return {'beta':np.nan,
                    'alpha':np.nan,
                    'alpha_t':np.nan,
                    'alpha_p':np.nan,
                    'beta_t':np.nan,
                    'beta_p':np.nan,
                    }
        X: pd.DataFrame = pd.concat([x, x], axis=1)
        X.columns = [0, 1]
        X[0][X[0] < 0] = 0
        X[1][X[1] > 0] = 0
        X['const'] = 1
        X2 = X.copy()
        est = sm.OLS(Y, X2)
        est2 = est.fit()
        return {'beta':est2.params[0] - est2.params[1],
                'alpha':est2.params.const,
                'alpha_t':est2.tvalues.const,
                'alpha_p':est2.pvalues.const,
                # TODO beta 2 - beta 1 , p values and t values calculation is not correct
                'beta_t':est2.tvalues[1],
                'beta_p':est2.pvalues[1]
                } 

    def _lambda_tm(self, x: pd.Series, fund_ret: pd.DataFrame):
        fund_id = x.name
        total = pd.concat({'Y': fund_ret[fund_id], 'x': x}, axis=1)
        total = total[total.notna().all(axis=1)]
        if total.empty:
            return {'beta':np.nan,
                    'alpha':np.nan,
                    'alpha_t':np.nan,
                    'alpha_p':np.nan,
                    'beta_t':np.nan,
                    'beta_p':np.nan,
                    }
        Y: pd.Series = total['Y']
        x = total['x']
        if x.count() != Y.count():
            return {'beta':np.nan,
                    'alpha':np.nan,
                    'alpha_t':np.nan,
                    'alpha_p':np.nan,
                    'beta_t':np.nan,
                    'beta_p':np.nan,
                    }
        X: pd.DataFrame = pd.concat([x, x*x], axis=1)
        X.columns = [0, 1]
        X['const'] = 1
        X2 = X.copy()
        est = sm.OLS(Y, X2)
        est2 = est.fit()
        return {'beta':est2.params[1],
                'alpha':est2.params.const,
                'alpha_t':est2.tvalues.const,
                'alpha_p':est2.pvalues.const,
                'beta_t':est2.tvalues[1],
                'beta_p':est2.pvalues[1]
                }  

    def _lambda_hm(self, x: pd.Series, fund_ret: pd.DataFrame):
        fund_id = x.name
        total = pd.concat({'Y': fund_ret[fund_id], 'x': x}, axis=1)
        total = total[total.notna().all(axis=1)]
        if total.empty:
            return {'beta':np.nan,
                    'alpha':np.nan,
                    'alpha_t':np.nan,
                    'alpha_p':np.nan,
                    'beta_t':np.nan,
                    'beta_p':np.nan,
                    }
        Y: pd.Series = total['Y']
        x = total['x']
        if x.count() != Y.count():
            return {'beta':np.nan,
                    'alpha':np.nan,
                    'alpha_t':np.nan,
                    'alpha_p':np.nan,
                    'beta_t':np.nan,
                    'beta_p':np.nan,
                    }
        X: pd.DataFrame = pd.concat([x, x], axis=1)
        X.columns = [0, 1]
        X[1][X[1] < 0] = 0
        X['const'] = 1
        X2 = X.copy()
        est = sm.OLS(Y, X2)
        est2 = est.fit()
        return {'beta':est2.params[1],
                'alpha':est2.params.const,
                'alpha_t':est2.tvalues.const,
                'alpha_p':est2.pvalues.const,
                'beta_t':est2.tvalues[1],
                'beta_p':est2.pvalues[1]
                }  

    def _lambda_alpha_beta(self, df_i):
        df_i = df_i.dropna()
        if sum(df_i.fund) == 0 or sum(df_i.benchmark) == 0:
            return {'alpha':np.Inf,'beta':np.Inf}
        else:
            std_x = df_i.benchmark.var()
            std_y = df_i.fund.var()
            if std_x  == 0:
                print('##########boom  x')
            if std_y == 0:
                print('##########boom  y')
            ploy_res = np.polyfit(y=df_i.fund, x=df_i.benchmark,deg=1)
            beta = ploy_res[0]
            alpha = ploy_res[1] * self._TRADING_DAYS_PER_YEAR
            return {'alpha':alpha,'beta':beta}

    def _get_benchmark_return(self) -> pd.DataFrame:
        benchmark_list: Dict[str, float] = {}
        fund_benchmark_df: pd.DataFrame = self._basic_api.get_fund_benchmark().drop(columns='_update_time')
        # 遍历每一只基金的benchmark进行处理
        for row in fund_benchmark_df.itertuples(index=False):
            values: List[pd.Series] = []
            cons: float = 0
            # 空的benchmark表明我们没有对应的指数或无法解析公式
            if row.benchmark_s:
                benchmark: Dict[str, float] = json.loads(row.benchmark_s)
                benchmark_raw: Dict[str, float] = eval(row.benchmark)
                for (index, weight), index_raw in zip(benchmark.items(), benchmark_raw.keys()):
                    if index == '1':
                        # 表示benchmark中该项为常数
                        cons += weight
                    elif index in ('ddir', 'nonor', 'tmd_1y', 'tmd_2y', 'tmd_3m', 'tmd_3y', 'tmd_5y', 'tmd_6m', 'tmd_7d'):
                    #elif str(index_raw).startswith('RA000'):
                        if weight == -1:
                            # 表示我们无法解析公式
                            print(f'[benchmark_return] Error: Need fix {row.fund_id} {index} {index_raw}')
                            self.log.append((row.fund_id, index))
                            break
                        else:
                            try:
                                ra: pd.Series = self._index_price.loc[:, index].copy()
                            except KeyError:
                                # 表示我们没有该指数的价格数据
                                print(f'[benchmark_return] Error: Data Missing: {row.fund_id} {index} {index_raw}')
                                self.log.append((row.fund_id, index))
                                break
                            else:
                                values.append(ra.iloc[1:] * 0.01 * weight)
                    else:
                        if weight == -1:
                            # 表示我们无法解析公式
                            print(f'[benchmark_return] Error: Need fix {row.fund_id} {index} {index_raw}')
                            self.log.append((row.fund_id, index))
                            break
                        else:
                            try:
                                ra: pd.Series = self._index_price.loc[:, index].copy()
                            except KeyError:
                                # 表示我们没有该指数的价格数据
                                print(f'Error: Data Missing: {row.fund_id} {index} {index_raw}')
                                self.log.append((row.fund_id, index))
                                break
                            else:
                                ra = np.log(ra).diff().iloc[1:]
                                values.append(ra * weight)
                else:
                    if values or cons:
                        the_sum: float = sum(values)
                        if cons:
                            the_sum += np.log(math.pow(1 + cons, 1 / self._TRADING_DAYS_PER_YEAR))
                        benchmark_list[row.fund_id] = the_sum

        return pd.DataFrame.from_dict(benchmark_list)

    def get_continue_stats_tool(self):
        type_list = self._fund_list.wind_class_2.unique().tolist()
        self.rank_dic = {}
        for t_i in type_list:
            _fund_list_type = self._fund_list[self._fund_list['wind_class_2'] == t_i].fund_id.tolist()
            fund_ret_columns = self._fund_ret.columns.tolist()
            _fl = [ i for i in fund_ret_columns if i in _fund_list_type]
            resample_ret = self.df_resample(self._fund_ret[_fl])
            rank_df = resample_ret.rank(pct=True,axis=1)
            self.rank_dic[t_i] = rank_df.copy()

    def get_scale(self, end_date, fund_id):
        try:
            scale = self._fund_size.loc[self.end_date,fund_id]
        except:
            scale = np.nan
        return scale

    def calculate_item(self, fund_id):
        wind_2_class = self._fund_list[self._fund_list['fund_id'] == fund_id].wind_class_2.values[0]

        sr = self._fund_nav[fund_id].dropna().tail(self._TRADING_DAYS_PER_YEAR)
        df_i = self._fund_ret[[fund_id]].rename(columns={fund_id:'fund'}).join(self._benchmark_ret[[fund_id]].rename(columns={fund_id:'benchmark'})).tail(self._TRADING_DAYS_PER_YEAR)
        _sr = self._fund_nav[fund_id]
        l = _sr.shape[0]
        _res = []
        for i in range(1,19,1):
            bloc = -l+20*(i-1)
            eloc = int(self._TRADING_DAYS_PER_YEAR/2)+-l+20*i
            _res.append(self._sharpe(_sr.iloc[bloc:eloc]))
        _res = [i for i in _res if i == i and i != np.inf and i != -np.inf]
        if len(_res) < 6:
            continue_regress_v = np.nan
            continue_regress_t = np.nan
        else:
            mod = AutoReg(_res, 1)
            res = mod.fit()
            continue_regress_v = res.params[0]
            continue_regress_t = res.tvalues[0]

        _rank_df = self.rank_dic[wind_2_class]
        res = []
        last = ''
        for idx,i in enumerate(_rank_df[fund_id]):
            now = 'W' if i > 0.5 else 'L'
            if idx != 0:
                res.append(last+now)
            last = now
        ww = max(res.count('WW'),1)
        ll = max(res.count('LL'),1)
        wl = max(res.count('WL'),1)
        lw = max(res.count('LW'),1)
        continue_stats_v = ww*ll/wl/lw

        res_i = self._lambda_alpha_beta(df_i)
        alpha = res_i['alpha']
        beta = res_i['beta']
        mdd_part =  sr[:] / sr[:].rolling(window=sr.shape[0], min_periods=1).max()
        mdd = 1 - mdd_part.min()
        annual_vol = (sr / sr.shift(1)).std(ddof=1) * np.sqrt(self._TRADING_DAYS_PER_YEAR)
        annual_ret = np.exp(np.log(sr.iloc[-1] / sr.fillna(method='bfill').iloc[0]) / sr.shape[0] * self._TRADING_DAYS_PER_YEAR) - 1
        sharpe = (annual_ret - self._RISK_FEE_RATE) / annual_vol
        treynor = (self._fund_ret.tail(self._TRADING_DAYS_PER_YEAR)[fund_id].mean() - self._RISK_FEE_RATE_PER_DAY)/beta
        calma_ratio = annual_ret / mdd if mdd != 0 else np.nan
        track_err = (df_i['fund'].tail(self._TRADING_DAYS_PER_YEAR) - df_i.tail(self._TRADING_DAYS_PER_YEAR)['benchmark']).std(ddof=1) * np.sqrt(self._TRADING_DAYS_PER_YEAR)
        info_ratio = alpha / track_err
        scale = self.get_scale(self.end_date,fund_id)
        stock_tm_res = self._lambda_tm(self._benchmark_ret.tail(self._TRADING_DAYS_PER_YEAR)[fund_id], self._fund_ret.tail(self._TRADING_DAYS_PER_YEAR))
        stutzer = self.stutzer_index(self._fund_ret.tail(self._TRADING_DAYS_PER_YEAR)[fund_id] - self._benchmark_ret.tail(self._TRADING_DAYS_PER_YEAR)[fund_id])['stutzer_index']
        
        stock_tm_alpha = stock_tm_res['alpha']
        stock_tm_alpha_t = stock_tm_res['alpha_t']
        stock_tm_alpha_p = stock_tm_res['alpha_p']
        stock_tm_beta = stock_tm_res['beta']
        stock_tm_beta_t = stock_tm_res['beta_t']
        stock_tm_beta_p = stock_tm_res['beta_p']

        stock_hm_res = self._lambda_hm(self._benchmark_ret.tail(self._TRADING_DAYS_PER_YEAR)[fund_id], self._fund_ret.tail(self._TRADING_DAYS_PER_YEAR))
        stock_hm_alpha = stock_hm_res['alpha']
        stock_hm_alpha_t = stock_hm_res['alpha_t']
        stock_hm_alpha_p = stock_hm_res['alpha_p']
        stock_hm_beta = stock_hm_res['beta']
        stock_hm_beta_t = stock_hm_res['beta_t']
        stock_hm_beta_p = stock_hm_res['beta_p']

        stock_cl_res = self._lambda_cl(self._benchmark_ret.tail(self._TRADING_DAYS_PER_YEAR)[fund_id], self._fund_ret.tail(self._TRADING_DAYS_PER_YEAR))
        stock_cl_alpha = stock_cl_res['alpha']
        stock_cl_alpha_t = stock_cl_res['alpha_t']
        stock_cl_alpha_p = stock_cl_res['alpha_p']
        stock_cl_beta = stock_cl_res['beta']
        stock_cl_beta_t = stock_cl_res['beta_t']
        stock_cl_beta_p = stock_cl_res['beta_p']
        
        return {
            'fund_id':fund_id,
            'datetime':self.end_date,
            'alpha':alpha,
            'beta':beta,
            'annual_vol':annual_vol,
            'annual_ret':annual_ret,
            'track_err':track_err,
            
            'continue_regress_v':continue_regress_v,
            'continue_regress_t':continue_regress_t,
            'continue_stats_v':continue_stats_v,

            'stock_cl_alpha':stock_cl_alpha,
            'stock_cl_alpha_t':stock_cl_alpha_t,
            'stock_cl_alpha_p':stock_cl_alpha_p,
            'stock_cl_beta':stock_cl_beta,
            'stock_cl_beta_t':stock_cl_beta_t,
            'stock_cl_beta_p':stock_cl_beta_p,

            'stock_tm_alpha':stock_tm_alpha,
            'stock_tm_alpha_t':stock_tm_alpha_t,
            'stock_tm_alpha_p':stock_tm_alpha_p,
            'stock_tm_beta':stock_tm_beta,
            'stock_tm_beta_t':stock_tm_beta_t,
            'stock_tm_beta_p':stock_tm_beta_p,

            'stock_hm_alpha':stock_hm_alpha,
            'stock_hm_alpha_t':stock_hm_alpha_t,
            'stock_hm_alpha_p':stock_hm_alpha_p,
            'stock_hm_beta':stock_hm_beta,
            'stock_hm_beta_t':stock_hm_beta_t,
            'stock_hm_beta_p':stock_hm_beta_p,
            'info_ratio':info_ratio,
            'treynor':treynor,
            'sharpe':sharpe,
            'calma_ratio':calma_ratio,
            'stutzer':stutzer,
            'scale':scale,
        }        

    def _sharpe(self, sr):
        annual_vol = (sr / sr.shift(1)).std(ddof=1) * np.sqrt(self._TRADING_DAYS_PER_YEAR)
        annual_ret = np.exp(np.log(sr.iloc[-1] / sr.iloc[0]) / sr.shape[0] * self._TRADING_DAYS_PER_YEAR) - 1
        sharpe = (annual_ret - self._RISK_FEE_RATE) / annual_vol
        return sharpe

    def calculate(self):
        self.res = []
        fund_list = self._fund_list[['fund_id','wind_class_1','wind_class_2']]
        _fund_list = self._fund_nav.columns.tolist()
        _fund_list_benchmark = self._benchmark_ret.columns.tolist()

        for i in fund_list.itertuples():
            if i.fund_id not in _fund_list or i.fund_id not in _fund_list_benchmark:
                continue
            self.res.append(self.calculate_item(i.fund_id))