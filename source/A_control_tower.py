from B_data_download import data_download
import C_preprocessing as pre
import D_strategy as str
import E_utils as util
import pandas as pd
pd.options.mode.chained_assignment = None

csv_path =  'csv_file/day_price_data.csv'
while True:
    ''' crawling data and read original price data '''
    data_download('day', 100, csv_path)

    ''' preprocessing '''
    before_day = 3
    ma_list = [5, 20]
    df = pre.read_price_data(csv_path)
    df = pre.n01_preprocessing_02(df, before_day, ma_list)

    ''' N01 strategy '''
    df = str.read_preprocessed_csv_file()
    n01_01 = str.n01_01_strategy(df)
    n01_02 = str.n01_02_strategy(df)

    ''' alerts '''
    util.stretagy_alert(n01_01)
    util.stretagy_alert(n01_02)
    time.sleep(86400)
