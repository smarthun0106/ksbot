from B_data_download import data_download
import C_preprocessing as pre
import D_strategy as str
import E_utils as util
import pandas as pd
import time
import os
pd.options.mode.chained_assignment = None

dir_name = 'csv_file'
try:
    # Create target Directory
    os.mkdir(dir_name)
    print("Directory " , dir_name ,  " Created ")
except FileExistsError:
    pass
csv_path_1 =  dir_name + '/day_price_data.csv'
csv_path_2 = dir_name + '/n01_preprocessed_csv_file.csv'

# while True:
''' Crawling data and read original price data '''
# data_download('day', 100, csv_path_1)

''' N01 '''
# Preprocessing
before_day = 3
ma_list = [5, 20]
df = pre.read_price_data(csv_path_1)
df = pre.n01_preprocessing_01(df, '005930', before_day, ma_list)
print(df)

# Strategy
# df = str.read_preprocessed_csv_file(csv_path_2)
# n01_01 = str.n01_01_strategy(df)
# n01_02 = str.n01_02_strategy(df)
# print(n01_01)

''' N02 '''
# Preprocessing
# Strategy

''' Alerts '''
# N01 alerts
# util.stretagy_alerta(n01_01)
# util.stretagy_alert(n01_02)

# N02 alerts

# time.sleep(86400)
