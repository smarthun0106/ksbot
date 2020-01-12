import pandas as pd

def read_preprocessed_csv_file(csv_path):
    df = pd.read_csv(csv_path, dtype={'code':str})
    df.index = df['code']
    df.drop(['code'], inplace=True, axis=1)
    return df

def n01_01_strategy(df):
    c0 = df['close'] > 0
    c1 = df['volume-1'] > 9000000
    c2 = df['volume'] < df['volume-1'] * 0.6
    c3 = (df['candle-1'] > 1.01) & (df['candle-1'] < 1.30)
    c4 = df['candle'] < 0.98
    c5 = (df['dcm-ma5'] > 0.98)  & (df['dcm-ma5'] < 1.00)

    df = df[c0 & c1 & c2 & c3 & c4 & c5]
    columns = ['name', 'date', 'candle', 'dcm-ma5']
    return df[columns]

def n01_02_strategy(df):
    c0 = df['close'] > 1000
    c1 = df['volume-2'] > 10000000
    c2 = df['volume-1'] < df['volume-2'] * 0.5
    c3 = df['volume'] < df['volume-1'] * 0.8
    c4 = df['candle-2'] > 1.04
    c5 = df['candle-1'] < 0.98
    c6 = df['candle'] < 0.99
    c7 = df['dcm-ma5'] < 1.02

    df = df[c0 & c1 & c2 & c3 & c4 & c5 & c6 & c7 ]
    columns = ['name', 'date', 'candle', 'dcm-ma5']
    return df[columns]
