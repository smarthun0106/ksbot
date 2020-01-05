import pandas as pd
import bs4
import requests
import time
pd.set_option('display.unicode.east_asian_width', True)

def get_price_all_data(firm_code, timeframe, count):
    url = "https://fchart.stock.naver.com"
    path = "/sise.nhn"
    parameters = {
        "symbol" : firm_code, "timeframe" : timeframe,
        "count" : count, "requestType" : 0
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

def get_all_features_data(firm_code,  firm_name, timeframe, count):
    url = "https://fchart.stock.naver.com"
    path = "/sise.nhn"
    parameters = {
        "symbol" : firm_code, "timeframe" : timeframe,
        "count" : count, "requestType" : 0
    }
    page = requests.get(url + path, params=parameters)
    price_data = bs4.BeautifulSoup(page.text, 'lxml')
    item_list = price_data.find_all('item')
    date_list = [] ; open_list = [] ;high_list = []
    low_list = [] ; close_list = [] ; volume_list = []
    for item in item_list:
        data = item["data"] ; datas = data.split("|")
        date_list.append(datas[0]) ; open_list.append(datas[1])
        high_list.append(datas[2]) ; low_list.append(datas[3])
        close_list.append(datas[4]) ; volume_list.append(datas[5])
    price_df = pd.DataFrame({
        'code' : firm_code, 'name' : firm_name,
        'date' : date_list, 'open' : open_list,
        'high' : high_list, 'low' : low_list,
        'close' : close_list, 'volume' : volume_list
    })
    return price_df

def crawling_firm_info():
    url = "http://kind.krx.co.kr"
    path = "/corpgeneral/corpList.do"
    parameters = {
        "method" : "download",
        "searchType" : "13"
    }
    page = requests.get(url+path, params=parameters)
    df = pd.read_html(page.text, header=0)[0]
    return df

def make_code(x):
    x = str(x)
    return '0'* (6-len(x)) + x

if __name__ == "__main__":
    firm_code_list = crawling_firm_info()["종목코드"]
    firm_code_list = firm_code_list.apply(make_code)
    firm_name_list = crawling_firm_info()["회사명"]

    ''' use def get_all_features_data('005930', '삼성전자', 'day', "365") '''
    for num, firm_code in enumerate(firm_code_list):
        try:
            print(num, firm_code, firm_name_list[num])
            time.sleep(1)
            try:
                price_df = get_all_features_data(firm_code, firm_name_list[num], "day", "500")
            except requests.exceptions.Timeout:
                time.sleep(60)
                price_df = get_all_features_data(firm_code, firm_name_list[num], "day", "500")
            if num == 0:
                total_price = price_df
            else:
                total_price = pd.concat([total_price, price_df])
        except KeyError:
            pass
        except ValueError:
            pass
    total_price.to_csv("price_data.csv")


# firm_code_list = crawling_firm_info()["종목코드"]
# firm_code_list = firm_code_list.apply(make_code)
#
# for num, firm_code in enumerate(firm_code_list):
#     try:
#         print(num, firm_code)
#         time.sleep(1)
#         try:
#             price_df = get_price_all_data(firm_code, "day", "1500")
#         except requests.exceptions.Timeout:
#             time.sleep(60)
#             price_df = get_price_all_data(firm_code, "day", "1500")
#         if num == 0:
#             total_price = price_df
#         else:
#             total_price = pd.merge(total_price, price_df, how="outer",
#                                    right_index=True, left_index=True)
#     except KeyError:
#         pass
#     except ValueError:
#         pass
# total_price.to_csv("price_data.csv")
