
import pandas as pd
import bs4
import requests
from loop_tools import concat_dataframe
from loop_tools import merge_dataframe

class CrawlingFirmPriceData(object):
    def __init__(self, timeframe, count, save_path, time_sleep=1):

        if timeframe != 'day' and timeframe != 'week' and timeframe != 'month':
            raise TypeError(f'you must put "day" or "week" or "month"')

        if not isinstance(count, int):
            raise TypeError(f'{count} must be int')

        if not save_path.endswith('.csv'):
            raise TypeError(f'{save_path} must be path with .csv')

        self.timeframe = timeframe
        self.count = count
        self.save_path = save_path
        self.time_sleep = time_sleep

    def crawling_type_a(self, firm_code, firm_name):
        url = "https://fchart.stock.naver.com"
        path = "/sise.nhn"
        parameters = {
            "symbol" : firm_code, "timeframe" : self.timeframe,
            "count" : self.count, "requestType" : 0
        }
        page = requests.get(url + path, params=parameters)
        price_data = bs4.BeautifulSoup(page.text, 'lxml')
        item_list = price_data.find_all('item')
        date_list = [] ; open_list = [] ;high_list = []
        low_list = [] ; close_list = [] ; volume_list = []
        for item in item_list:
            data = item["data"]
            datas = data.split("|")
            date_list.append(datas[0])
            open_list.append(datas[1])
            high_list.append(datas[2])
            low_list.append(datas[3])
            close_list.append(datas[4])
            volume_list.append(datas[5])
        price_df = pd.DataFrame({
            'code' : firm_code, 'name' : firm_name,
            'date' : date_list, 'open' : open_list,
            'high' : high_list, 'low' : low_list,
            'close' : close_list, 'volume' : volume_list
        })
        return price_df

    def crawling_type_b(self, firm_code):
        url = "https://fchart.stock.naver.com"
        path = "/sise.nhn"
        parameters = {
            "symbol" : firm_code, "timeframe" : self.timeframe,
            "count" : self.count, "requestType" : 0
        }
        page = requests.get(url + path, params=parameters)
        price_data = bs4.BeautifulSoup(page.text, 'lxml')
        item_list = price_data.find_all('item')
        date_list = []
        price_list = []
        for item in item_list:
            data = item["data"]
            datas = data.split("|")
            date_list.append(datas[0])
            price_list.append(datas[4])
        price_df = pd.DataFrame({firm_code : price_list}, index=date_list)
        return price_df

    def run_a(self):
        total_price = concat_dataframe(self.crawling_type_a, self.time_sleep)
        total_price.to_csv(self.save_path)
        return total_price

    def run_b(self):
        total_price = merge_dataframe(self.crawling_type_b, self.time_sleep)
        total_price.to_csv(self.save_path)
        return total_price

if __name__ == "__main__":
    save_path = 'abc.csv'
    CrawlingFirmPriceData('day', 100, save_path=save_path, time_sleep=1.0)
