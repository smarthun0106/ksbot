import pandas as pd
import numpy as np
pd.set_option('display.unicode.east_asian_width', True)


''' read csv price data '''
def read_price_csv(path):
    df = pd.read_csv(path, dtype={'INDEX':str}, index_col=["Unnamed: 0"])
    df.index = df.index.astype(str)
    df.index = pd.to_datetime(df.index)
    return df

''' get momentum rank '''
def get_momentum_rank(price_df, index_date, date_range, num):
    momentum_df = pd.DataFrame(price_df.pct_change(date_range).loc[index_date])
    momentum_df.columns = ['momentum']
    momentum_df['momentum_rank'] = momentum_df['momentum'].rank(ascending=False)
    momentum_df = momentum_df.sort_values(by='momentum_rank')
    return momentum_df[:num]

''' Load Data '''
# price_df = read_price_csv("price_data.csv")
# momentum_rank_df = get_momentum_rank(price_df, '2016-12-29', 250, 20)
# print(momentum_rank_df)
