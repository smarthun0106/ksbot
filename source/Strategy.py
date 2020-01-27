import pandas as pd
import numpy as np
import warnings
import inspect
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None
pd.set_option('display.unicode.east_asian_width', True)

class N01:
    def __init__(self, back_tested_path, pre_csv_path, ratio=0.93):
        self.back_tested_path = back_tested_path
        self.pre_csv_path = pre_csv_path

        self.back_df = pd.read_csv(back_tested_path, dtype={'code':str})

        pre_df = pd.read_csv(pre_csv_path, dtype={'code':str}, parse_dates=['date'])
        pre_df.index = pre_df['code']
        pre_df.drop(['code'], inplace=True, axis=1)
        self.pre_df = pre_df

        self.ratio = ratio

    def back_df_pre(self):
        df = self.back_df
        df = df[df['gt_1.015'] >= self.ratio]
        return df

    def get_mean(self, df, firm_code):
        df = df.loc[firm_code]
        df['gt_1.015_mean'] = df['gt_1.015'].mean()
        df['gt_1.025_mean'] = df['gt_1.025'].mean()
        df['gt_1.035_mean'] = df['gt_1.035'].mean()
        df['gt_1.045_mean'] = df['gt_1.045'].mean()
        return df.iloc[-1:]

    def n01(self, pre_df, con):
        c0 = pre_df['close'] > con['cp']
        c1 = pre_df['volume-1'] > con['bv']
        c2 = pre_df['volume'] < pre_df['volume-1'] * con['bv_rate']
        c3 = (pre_df['candle-1'] > con['min_bc']) & (pre_df['candle-1'] < con['max_bc'])
        c4 = pre_df['candle'] < con['ac1']
        c5 = (pre_df['close/ma5'] > con['min_cm_rate'])  & (pre_df['close/ma5'] < con['max_cm_rate'])
        pre_df = pre_df[c0 & c1 & c2 & c3 & c4 & c5]
        pre_df['test_code'] = con['test_code']
        pre_df['gt_1.015'] = con['gt_1.015']
        pre_df['gt_1.025'] = con['gt_1.025']
        pre_df['gt_1.035'] = con['gt_1.035']
        pre_df['gt_1.045'] = con['gt_1.045']
        columns = [
            'name', 'date', 'test_code',
            'gt_1.015', 'gt_1.025', 'gt_1.035', 'gt_1.045'
        ]
        return pre_df[columns]

    def run(self):
        pre_df = self.pre_df
        back_df = self.back_df_pre()
        for index in range(back_df.shape[0]):
            one_condition = back_df.iloc[index]
            n01 = self.n01(pre_df, one_condition)
            if index == 0:
                result_df = n01
            else:
                result_df = pd.concat([result_df, n01])

        firm_codes = result_df.index.drop_duplicates(keep='first')
        print(firm_codes)
        for num, firm_code in enumerate(firm_codes):
            result_df_firm = self.get_mean(result_df, firm_code)
            if num == 0:
                final_df = result_df_firm
            else:
                final_df = pd.concat([final_df, result_df_firm])
        columns = [
            'name', 'date', 'gt_1.015_mean',
            'gt_1.025_mean', 'gt_1.035_mean', 'gt_1.045_mean'
        ]
        return final_df[columns]


if __name__ == "__main__":
    pass


    # strategy_pre = StrategyPreprocessing()
    # df = strategy_pre.n01_pre_one(df, '100840')
    #
    # my_strategy = Strategy()
    # df = my_strategy.n01_01(csv_path)
    # print(df)
