import pandas as pd

def read_preprocessed_csv_file():
    df = pd.read_csv('csv_file/preprocessed_csv_file.csv', dtype={'code':str})
    df.index = df['code']
    df.drop(['code'], inplace=True, axis=1)
    return df

def n01_01_strategy(df):
    c0 = df['close'] > 1000
    c1 = df['volume-1'] > 10000000
    c2 = df['volume'] < df['volume-1'] * 0.5
    c3 = df['candle'] < 0.975
    c4 = df['dcm-ma5'] < 1.01

    df = df[c0 & c1 & c2 & c3 & c4]
    columns = ['name', 'date', 'candle', 'dcm-ma5']
    return df[columns]

def n01_02_strategy(df):
    c0 = df['close'] > 1000
    c1 = df['volume-2'] > 10000000
    c2 = df['volume-1'] < df['volume-2'] * 0.5
    c3 = df['volume'] < df['volume-1'] * 0.8
    c4 = df['candle-1'] < 0.975
    c5 = df['candle'] < 0.99
    c6 = df['dcm-ma5'] < 1.019

    df = df[c0 & c1 & c2 & c3 & c4 & c5 & c6 ]
    columns = ['name', 'date', 'candle', 'dcm-ma5']
    return df[columns]

def n01_03_strategy(df):
    # c0 = df['close'] > 1000
    c1 = df['volume-3'] > 10000000
    c2 = df['volume-2'] < df['volume-3'] * 0.5
    c3 = df['volume-1'] < df['volume-2'] * 0.8
    c4 = df['volume'] < df['volume-1'] * 0.8
    # c5 = df['candle'] < 0.995
    # c6 = df['dcm-ma5'] < 1.01

    df = df[ c1 & c2 & c3 & c4  ]
    columns = ['name', 'date', 'candle', 'dcm-ma5']
    return df[columns]
