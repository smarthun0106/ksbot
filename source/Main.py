import time
import datetime

import settings
from ks_price_data import CrawlingFirmPriceData
from preprocessing import N01Pre
from strategy import N01

def n01_run(mode):
    raw_data_path = 'csv_file/raw_day_price.csv'
    n01_pre_data_path = 'csv_file/n01_pre_price.csv'
    n01_back_test_path = 'BackTesting/csv_file_test/n01/' + \
                         'n01_result_2020-01-23_21_14_44.csv'

    if mode == 0:
        crawling_raw_data = CrawlingFirmPriceData('day',
                                                  100,
                                                  save_path=raw_data_path,
                                                  time_sleep=1.0).run_a()
        return crawling_raw_data

    if mode == 1:
        n01_pre = N01Pre(raw_data_path, n01_pre_data_path).run()
        return n01_pre

    if mode == 2:
        n01_set = N01(n01_back_test_path, n01_pre_data_path, ratio=0.95)
        n01_firms = n01_set.run()
        return n01_firms

    if mode == 3:
        crawling_raw_data = CrawlingFirmPriceData('day',
                                                  100,
                                                  save_path=raw_data_path,
                                                  time_sleep=0.8).run_a()
        n01_pre = N01Pre(raw_data_path, n01_pre_data_path).run()
        n01_set = N01(n01_back_test_path, n01_pre_data_path, ratio=0.90)
        n01_firms = n01_set.run()
        return n01_firms

if __name__ == "__main__":
    mode = input('mode : ')
    n01 = n01_run(mode=int(mode))
    print(n01)
