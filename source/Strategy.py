import pandas as pd
import numpy as np
import warnings
import inspect
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None
pd.set_option('display.unicode.east_asian_width', True)

class N01:
    def __init__(self, back_test_result_path, pre_csv_path):
        self.pre = PreprocessingTools()
        self.back_tested_df = pd.read_csv(back_test_result_path)
        self.pre_csv_path = pre_csv_path

    def find_gt_df(self, df, gt_name, ratio):
        df = df[df[gt_name] >= ratio]
        return df

    def n01_back_test_analysis(self):
        columns = [
            'min_cm_rate', 'min_bc', 'max_cm_rate', 'max_bc', 'invest_day',
            'cp', 'cm', 'bv_rate', 'bv', 'ac2', 'ac1', 'firm_number',
            'gt_1.015', 'gt_1.025', 'gt_1.035', 'gt_1.045', 'test_code'
        ]
        df = self.back_tested_df[columns]
        df = self.find_gt_df(df, 'gt_1.015', 0.93)
        return df

    def get_mean(self, df, firm_code):
        df = df.loc[firm_code]
        df['gt_1.015_mean'] = df['gt_1.015'].mean()
        df['gt_1.025_mean'] = df['gt_1.025'].mean()
        df['gt_1.035_mean'] = df['gt_1.035'].mean()
        df['gt_1.045_mean'] = df['gt_1.045'].mean()
        return df

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
        return pre_df[['name', 'date', 'test_code', 'gt_1.015', 'gt_1.025', 'gt_1.035', 'gt_1.045']]

    def n01_loop(self):
        pre_df = self.pre.read_csv(self.pre_csv_path)
        back_df = self.n01_back_test_analysis()
        for index in range(back_df.shape[0]):
            one_condition = back_df.iloc[index]
            n01 = self.n01(pre_df, one_condition)
            if index == 0:
                result_df = n01
            else:
                result_df = pd.concat([result_df, n01])

        firm_codes = result_df.index.drop_duplicates(keep='first')
        for num, firm_code in enumerate(firm_codes):
            result_df = self.get_mean(result_df, firm_code)
            if num == 0:
                final_df = result_df
            else:
                final_df = pd.concat([final_df, result_df])
        return final_df


if __name__ == "__main__":
    back_test_result_path = 'BackTesting/csv_file_test/n01/'
    back_test_csv_name = 'n01_result_2020-01-23_21_14_44.csv'
    n01_pre_all_path = 'csv_file/n01_pre_all.csv'
    n01 = N01(back_test_result_path + back_test_csv_name, n01_pre_all_path)
    print(n01.n01_loop())


    # strategy_pre = StrategyPreprocessing()
    # df = strategy_pre.n01_pre_one(df, '100840')
    #
    # my_strategy = Strategy()
    # df = my_strategy.n01_01(csv_path)
    # print(df)
