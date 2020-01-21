import os
import time
import datetime

from KsDataFrame import PriceData
from Strategy import StrategyPreprocessing, Strategies
from Utils import Alert


dir_name = 'csv_file'
try:
    # Create target Directory
    os.mkdir(dir_name)
    print("Directory " , dir_name ,  " Created ")
except FileExistsError:
    pass

turn_on = True
while True:
    time.sleep(1)
    now = datetime.datetime.now()
    day = now.weekday()
    hour = int(now.strftime('%H'))
    if hour >= 16 and day <= 4 and turn_on:
        # set path
        day_price_path = 'csv_file/day_price_data.csv'
        n01_pre_all_path = 'csv_file/n01_pre_all.csv'

        # crawling price data
        PriceData().price_datas('day', 100, day_price_path)

        # preprocessing data
        StrategyPreprocessing().n01_pre_all(day_price_path)

        # strategy
        n01_01 = Strategies().n01_01(n01_pre_all_path)

        # alert
        Alert().stretagy_alert(n01_01)
        turn_on = False

    if hour == 1:
        turn_on = True

    # day_price_path = 'csv_file/day_price_data.csv'
    # n01_pre_all_path = 'csv_file/n01_pre_all.csv'
    #
    # # crawling price data
    # PriceData().price_datas('day', 100, day_price_path)
    #
    # # preprocessing data
    # StrategyPreprocessing().n01_pre_all(day_price_path)
    #
    # # strategy
    # n01_01 = Strategies().n01_01(n01_pre_all_path)
    #
    # # alert
    # Alert().stretagy_alert(n01_01)
    # turn_on = False
