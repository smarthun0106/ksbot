import pandas as pd
import numpy as np
import warnings
import inspect
from KsDataFrame import PriceData
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None
pd.set_option('display.unicode.east_asian_width', True)

class PreprocessingTools:
    def __init__(self):
        pass

    def firm_codes(self):
        price_data = PriceData()
        firm_codes = price_data.crawling_firm_info()['종목코드']
        firm_codes = firm_codes.apply(price_data.make_code)
        return firm_codes

    def read_csv(self, csv_path):
        df = pd.read_csv(csv_path, dtype={'code':str}, parse_dates=['date'])
        df.index = df['code']
        df.drop(['code'], inplace=True, axis=1)
        return df

    def shift_data(self, df, feature_names, days, type):
        days = days+1
        for feature_name in feature_names:
            if type == 'before':
                for day in range(1, days):
                    new_feature_name = feature_name + '-' + str(day)
                    df.loc[:, new_feature_name] = df[feature_name].shift(day)
            if type == 'after':
                for day in range(1, days):
                    new_feature_name = feature_name + '+' + str(day)
                    df.loc[:, new_feature_name] = df[feature_name].shift(-day)
        df.dropna(inplace=True)
        return df

    def moving_average(self, df, ma_feature, ma_list):
        for num, ma in enumerate(ma_list):
            ma_name = 'ma'+str(ma)
            df.loc[:, ma_name] = df[ma_feature].rolling(ma).mean()
        df.dropna(inplace=True)
        return df

    def ratio_close_ma(self, df, ratio_name, ma):
        df.loc[:, ratio_name] = df['close'] / df[ma]
        return df

    def ratio_candle(self, df):
        df.loc[:, 'candle'] = df['close'] / df['open']
        return df

    def time_splite(self, df):
        df.loc[:, 'year'] = df['date'].dt.year
        df.loc[:, 'month'] = df['date'].dt.month
        df.loc[:, 'day'] = df['date'].dt.day
        df.loc[:, 'hour'] = df['date'].dt.hour
        df.loc[:, 'minute'] = df['date'].dt.minute
        df.loc[:, 'second'] = df['date'].dt.second
        return df

    def pre_all(self, df, pre_method):
        firm_codes = self.firm_codes()
        for num, firm_code in enumerate(firm_codes):
            try:
                one_firm_df = pre_method(df, firm_code)
                if num == 0:
                    all_firms_df = one_firm_df
                else:
                    all_firms_df = pd.concat([all_firms_df, one_firm_df])
                print('{0}/{1} {2} 완료'.format(num, len(firm_codes), firm_code))
            except KeyError:
                pass
            except AttributeError:
                pass
        return all_firms_df



class StrategyPreprocessing:
    def __init__(self):
        price_data = PriceData()
        firm_infos = price_data.crawling_firm_info()['종목코드']
        self.firm_codes = firm_infos.apply(price_data.make_code)
        self.pre = PreprocessingTools()

    def n01_pre_one(self, df, firm_code):
        pre = self.pre
        df = df.loc[firm_code]
        df = pre.moving_average(df, 'close', [5])
        df = pre.ratio_candle(df)
        df = pre.ratio_close_ma(df, 'close/ma5', 'ma5')
        df = pre.shift_data(df, ['volume', 'candle'], 3, 'before')
        return df.iloc[-1:]

    def n01_pre_all(self, csv_path):
        firm_codes = self.firm_codes
        df = self.pre.read_csv(csv_path)

        for num, firm_code in enumerate(firm_codes):
            try:
                one_firm_df = self.n01_pre_one(df, firm_code)
                if num == 0:
                    all_firms_df = one_firm_df
                else:
                    all_firms_df = pd.concat([all_firms_df, one_firm_df])
                print('{0}/{1} {2} 완료'.format(num, len(firm_codes), firm_code))
            except KeyError:
                pass
            except AttributeError:
                pass

        func_name = inspect.currentframe().f_code.co_name
        csv_name = func_name + '.csv'
        csv_path = 'csv_file/' + csv_name
        all_firms_df.to_csv(csv_path)

class Strategies:
    def __init__(self):
        self.pre = PreprocessingTools()

    '''
    n01_02_result_2020-01-21_20_56_56
    cp	         bv	bv_rate	  min_bc	max_bc	ac1	   ac2	cm	       min_cm_rate	max_cm_rate	invest_day	firm_number	  win_rate	ror	            test_code
    1000	9000000	    0.6	    1.01	   1.3	0.99   1.0	close/ma5-1       0.97	      1.005	         5	        216	     0.731	7039	n01_02strategy476
    '''
    def n01_01(self, csv_path):
        df = self.pre.read_csv(csv_path)
        c0 = df['close'] > 1000
        c1 = df['volume-1'] > 9000000
        c2 = df['volume'] < df['volume-1'] * 0.6
        c3 = (df['candle-1'] > 1.01) & (df['candle-1'] < 1.30)
        c4 = df['candle'] < 0.99
        c5 = (df['close/ma5'] > 0.970)  & (df['close/ma5'] < 1.005)
        df = df[c0 & c1 & c2 & c3 & c4 & c5]
        return df


if __name__ == "__main__":
    day_price_path = 'csv_file/day_price_data.csv'
    tool = PreprocessingTools()
    df = tool.read_csv(day_price_path)
    # strategy_pre = StrategyPreprocessing()
    # df = strategy_pre.n01_pre_one(df, '100840')
    #
    # my_strategy = Strategy()
    # df = my_strategy.n01_01(csv_path)
    # print(df)
