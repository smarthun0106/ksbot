import pandas as pd
import numpy as np
import sub_source.firms_price_dataframe as gp

def read_price_data(csv_path):
    df = pd.read_csv(csv_path, dtype={'code':str}, parse_dates=['date'])
    df.index = df['code']
    df.drop(['code'], inplace=True, axis=1)
    return df

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

    return df[-1:]

def n01_preprocessing_02(df, before_day, ma_list):
    firm_code_list = gp.crawling_firm_info()["종목코드"]
    firm_code_list = firm_code_list.apply(gp.make_code)
    for num, firm_code in enumerate(firm_code_list):
        p_df = n01_preprocessing_01(df, firm_code, before_day, ma_list)
        if num == 0:
            preprocessed_df = p_df
        else:
            preprocessed_df = pd.concat([preprocessed_df, p_df])
    preprocessed_df.to_csv('csv_file/preprocessed_csv_file.csv')
    return preprocessed_df
