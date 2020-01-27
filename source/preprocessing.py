import pandas as pd
import numpy as np
import warnings
import inspect

from loop_tools import concat_dataframe
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None
pd.set_option('display.unicode.east_asian_width', True)

class PreprocessingTools:
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

class N01Pre:
    def __init__(self, load_path, save_path):
        self.pre = PreprocessingTools()
        self.df = self.pre.read_csv(load_path)
        self.save_path = save_path

    def n01_pre_set(self, firm_code, firm_name):
        pre = self.pre
        df = self.df
        df = df.loc[firm_code]
        df = pre.moving_average(df, 'close', [5])
        df = pre.ratio_candle(df)
        df = pre.ratio_close_ma(df, 'close/ma5', 'ma5')
        df = pre.shift_data(df, ['volume', 'candle'], 3, 'before')
        return df.iloc[-1:]

    def run(self):
        result_df = concat_dataframe(self.n01_pre_set, 0)
        result_df.to_csv(self.save_path)
        return result_df

if __name__ == "__main__":
    n01 = N01Pre('csv_file/day_price_data.csv').run()
    print(n01)
