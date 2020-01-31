import pandas as pd
import requests
import time

def make_code(x):
    x = str(x)
    return '0'* (6-len(x)) + x

def crawling_firm_info():
    url = "http://kind.krx.co.kr"
    path = "/corpgeneral/corpList.do"
    parameters = {
        "method" : "download",
        "searchType" : "13"
    }
    page = requests.get(url+path, params=parameters)
    df = pd.read_html(page.text, header=0)[0]
    firm_codes = df['종목코드']
    firm_codes = firm_codes.apply(make_code)
    firm_names = df['회사명']
    return firm_codes, firm_names

def concat_dataframe(func, time_sleep):
    firm_codes, firm_names = crawling_firm_info()
    for num, firm_code in enumerate(firm_codes):
        try:
            time.sleep(time_sleep)
            try:
                price_df = func(firm_code, firm_names[num])
            except requests.exceptions.Timeout:
                time.sleep(60)
                price_df = func(firm_code, firm_names[num])
            if num == 0:
                total_price = price_df
            else:
                total_price = pd.concat([total_price, price_df])
            print(f"{num}/{len(firm_codes)-1} {firm_code} DONE")
        except KeyError:
            pass
        except ValueError:
            pass
        except AttributeError:
            pass
    return total_price

def merge_dataframe(func, time_sleep):
    firm_codes, firm_names = crawling_firm_info()
    for num, firm_code in enumerate(firm_codes):
        try:
            time.sleep(time_sleep)
            try:
                price_df = func(firm_code)
            except requests.exceptions.Timeout:
                time.sleep(60)
                price_df = func(firm_code)
            if num == 0:
                total_price = price_df
            else:
                total_price = pd.merge(total_price, price_df, how="outer",
                                       right_index=True, left_index=True)
            print(f"{num}/{len(firm_codes)-1} {firm_code} DONE")
        except KeyError:
            pass
        except ValueError:
            pass
    return total_price
