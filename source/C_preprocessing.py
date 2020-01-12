import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import get_firms_price_dataframe as gp

import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None

def read_price_data(csv_path):
    df = pd.read_csv(csv_path, dtype={'code':str}, parse_dates=['date'])
    df.index = df['code']
    df.drop(['code'], inplace=True, axis=1)
    return df

''' N01 Stretagy Preprocessing '''
def n01_preprocessing_01(df, firm_code, before_day, ma_list):
    df = df.loc[firm_code]
    before_day = before_day + 1

    # add volume information
    for i in range(1, before_day):
        df.loc[:, 'volume' + str(-i)] = df['volume'].shift(i)

    # add candle information
    for i in range(before_day):
        if i == 0:
            df.loc[:, 'candle'] = df['close'] / df['open']
            df['candle'] = np.around(df['candle'], decimals=4)
        else:
            df.loc[:, 'candle' + str(-i)] = df['candle'].shift(i)
            df['candle' + str(-i)] = np.around(df['candle' + str(-i)], decimals=4)

    # add moving average
    for num, ma in enumerate(ma_list):
        ma_name = 'ma'+str(ma)
        df.loc[:, ma_name] = df['close'].rolling(ma).mean()
        df.loc[:, 'dcm'+'-ma'+ str(ma)] = df['close'] / df[ma_name]
        df['dcm'+'-ma'+ str(ma)] = np.around(df['dcm'+'-ma'+ str(ma)], decimals=4)
    df.dropna(inplace=True)
    return df.iloc[-1:]

def n01_preprocessing_02(df, before_day, ma_list):
    firm_code_list = gp.crawling_firm_info()["종목코드"]
    firm_code_list = firm_code_list.apply(gp.make_code)
    for num, firm_code in enumerate(firm_code_list):
        p_df = n01_preprocessing_01(df, firm_code, before_day, ma_list)
        if num == 0:
            preprocessed_df = p_df
        else:
            preprocessed_df = pd.concat([preprocessed_df, p_df])
        print('{0}/{1} {2} 완료'.format(num, len(firm_code_list), firm_code))
    preprocessed_df.to_csv('csv_file/n01_preprocessed_csv_file.csv')
    return preprocessed_df

''' N02 Stretagy Preprocessing '''
def n02_preprocessing_01(df, firm_code, alpha):
    df = df.loc[firm_code]
    df.loc[:, 'av'] = df['close'].mean()
    df['close-av'] = df['av'] - df['close']
    find_low_price_df = df.sort_values(by=['close-av'], ascending=False)
    df['low_result'] = find_low_price_df['close'].iloc[:alpha].mean()
    df.loc[:, 'start_month'] = df['date'].dt.month
    df = df.sort_values(by='start_month')
    df.loc[:, 'candle'] = df['close'] / df['open']
    return df

def n02_preprocessing_02(df, alpha, month, candle, option):
    firm_code_list = gp.crawling_firm_info()["종목코드"]
    firm_code_list = firm_code_list.apply(gp.make_code)

    result_df = pd.DataFrame(columns=['code', 'name'])
    for num, firm_code in enumerate(firm_code_list):
        n02_df = n02_preprocessing_01(df, firm_code, alpha)

        if option == 1:
            c1 = n02_df['start_month'] == month
            c2 = n02_df['start_month'] == month + 1
            n02_df = n02_df[c1 | c2]
            c3 = n02_df['candle'] > candle
            result_num = n02_df[c3].shape[0]
            num = 8
        elif option == 2:
            c1 = n02_df['start_month'] == month
            c2 = n02_df['candle'] > candle
            result_num = n02_df[c1 & c2].shape[0]
            num = 4

        if result_num == num:
            result_df = result_df.append({
                'code' : firm_code,
                'name' : n02_df['name'].iloc[0],
                'low_result' : n02_df['low_result'].iloc[0],
            }, ignore_index=True)
    return result_df


''' Test '''
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    # # N01 test
    # before_day = 3
    # ma_list = [5, 20]
    # df = read_price_data('csv_file/day_price_data.csv')
    # df = n01_preprocessing_01(df, '005930', before_day, ma_list)
    # print(df[['candle', 'candle-1', 'candle-2']])


    # N02 test
    df = read_price_data('csv_file/month_price_data.csv')
    df = n02_preprocessing_02(df, alpha=10, month=3, candle=1.05, option=2)
    print(df)


    # plt.plot(df['date'], df['close'])
    # plt.plot(df['date'], df['av'])
    # plt.plot(df['date'], df['low_result'], label='low')
    # plt.legend()
    # plt.show()
