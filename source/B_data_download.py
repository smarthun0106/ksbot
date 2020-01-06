import sub_source.firms_price_dataframe as gp
import pandas as pd
import numpy as np
import time
import requests
pd.set_option('display.unicode.east_asian_width', True)
pd.options.mode.chained_assignment = None

def data_download(timeframe, count, csv_path):
    firm_code_list = gp.crawling_firm_info()["종목코드"]
    firm_code_list = firm_code_list.apply(gp.make_code)
    firm_name_list = gp.crawling_firm_info()["회사명"]

    ''' use def get_all_features_data('005930', '삼성전자', 'day', "365") '''
    for num, firm_code in enumerate(firm_code_list):
        try:
            print(num, firm_code, firm_name_list[num])
            time.sleep(1)
            try:
                price_df = gp.get_all_features_data(firm_code, firm_name_list[num], timeframe, count)
            except requests.exceptions.Timeout:
                time.sleep(60)
                price_df = gp.get_all_features_data(firm_code, firm_name_list[num],timeframe, count)
            if num == 0:
                total_price = price_df
            else:
                total_price = pd.concat([total_price, price_df])
        except KeyError:
            pass
        except ValueError:
            pass
    total_price.to_csv(csv_path, index=False)
