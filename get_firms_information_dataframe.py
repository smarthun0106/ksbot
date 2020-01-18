import pandas as pd
import requests
import time

''' Preprocessing Balance Sheet '''
def make_fs_table_clear(df):
    temp_df1 = df[0]
    temp_df1 = temp_df1.set_index(temp_df1.columns[0])
    temp_df1 = temp_df1[temp_df1.columns[:4]]
    temp_df1 = temp_df1.loc[["매출액", "영업이익", "당기순이익"]]

    temp_df2 = df[2]
    temp_df2 = temp_df2.set_index(temp_df2.columns[0])
    temp_df2 = temp_df2.loc[["자산", "부채", "자본"]]

    temp_df3 = df[4]
    temp_df3 = temp_df3.set_index(temp_df3.columns[0])
    temp_df3 = temp_df3.loc[["영업활동으로인한현금흐름"]]

    fs_df = pd.concat([temp_df1, temp_df2, temp_df3])
    return fs_df

''' Preprocessing Balance Sheet Ratio '''
def make_fr_table_clear(df):
    df = df[0]
    df = df.set_index(df.columns[0])
    df = df.loc[[
        "유동비율계산에 참여한 계정 펼치기",
        "유보율계산에 참여한 계정 펼치기",
        "부채비율계산에 참여한 계정 펼치기",
        "매출액증가율계산에 참여한 계정 펼치기",
        "영업이익률계산에 참여한 계정 펼치기",
        "ROA계산에 참여한 계정 펼치기",
        "ROE계산에 참여한 계정 펼치기",
        "ROIC계산에 참여한 계정 펼치기"
    ]]
    df.index = ["유동비율", "유보율", "부채비율",
                "매출증가율", "영업이익율", "ROA", "ROE", "ROIC"]
    return df

def make_invest_table_clear(df):
    df = df[1]
    df = df.set_index(df.columns[0])
    df = df.loc[[
        "PER계산에 참여한 계정 펼치기",
        "PCR계산에 참여한 계정 펼치기",
        "PSR계산에 참여한 계정 펼치기",
        "PBR계산에 참여한 계정 펼치기",
    ]]
    df.index = ["PER", "PCR", "PSR", "PBR"]
    return df

'''
crawling data from https://comp.fnguide.com/
Balance Sheet : 1, https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A002700&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701
Balance Sheet Ratio : 2, https://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode=A002700&cID=&MenuYn=Y&ReportGB=&NewMenuID=104&stkGb=701
Invetment Index : 3, https://comp.fnguide.com/SVO2/ASP/SVD_Invest.asp?pGB=1&gicode=A002700&cID=&MenuYn=Y&ReportGB=&NewMenuID=105&stkGb=701
'''
def make_crawling_dataframe(firm_code, option):
    pd.set_option('display.unicode.east_asian_width', True)

    if option == 1:
        fs_path = "/SVO2/ASP/SVD_Finance.asp"
    elif option == 2:
        fs_path = "/SVO2/ASP/SVD_FinanceRatio.asp"
    elif option == 3:
        fs_path = "/SVO2/ASP/SVD_Invest.asp?"

    fs_url = "https://comp.fnguide.com"
    parameters = {
        "pGB" : 1, "gicode" : firm_code,
        "cID" : "", "MenuYn" : "Y",
        "ReportGB" : "D", "NewMenuID" : 103,
        "stkGb" : 701
    }
    fs_page = requests.get(fs_url + fs_path, params=parameters)
    fs_table = pd.read_html(fs_page.text)

    if option == 1:
        fs_table = make_fs_table_clear(fs_table)
    elif option ==2:
        fs_table = make_fr_table_clear(fs_table)
    elif option ==3:
        fs_table = make_invest_table_clear(fs_table)
    return fs_table

''' make dataframe more visiable '''
def transform_data(firm_code, df):
    for num, col in enumerate(df.columns):
        temp_df = pd.DataFrame({firm_code : df[col]})
        temp_df = temp_df.T
        temp_df.columns = [[col]*len(df), temp_df.columns]
        if num == 0:
            total_df = temp_df
        else:
            total_df = pd.merge(total_df, temp_df, how="outer",
                                left_index=True, right_index=True)
    return total_df

''' get all firms data '''
def get_all_firms_data(firm_codes_list, option):
    for num, firm_code in enumerate(firm_codes_list):
        try:
            fsb_df = make_crawling_dataframe(firm_code, option)
            fsb_df_changed = transform_data(firm_code, fsb_df)
            if num == 0:
                total_fs = fsb_df_changed
            else:
                total_fs = pd.concat([total_fs, fsb_df_changed])
            print("{0} {1} 완료".format(num, firm_code))
            time.sleep(1)
        except requests.exceptions.Timeout:
            time.sleep(60)
            pass
        except KeyError:
            pass
        except ValueError:
            pass
    return total_fs

''' crawling firm codes and any information '''
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

''' convert firm code into Axxxxxx '''
def make_code(x):
    x = str(x)
    return 'A' + '0'* (6-len(x)) + x

def make_firm_codes_clear():
    df = crawling_firm_info()
    df["종목코드"] = df["종목코드"].apply(make_code)
    df.rename(index=df["종목코드"], inplace=True)
    df.drop("종목코드", axis=1, inplace=True)
    df.columns = pd.MultiIndex.from_product([df.columns, ['']])
    return df

''' merge firm balance sheet information and firm informations '''
def merge_two_dataframe(firm_info, firm_f, csv=None):
    total_df = pd.merge(firm_f, firm_info, how="outer", left_index=True, right_index=True)
    if csv:
        total_df.to_csv(csv)
    return total_df


firm_info = make_firm_codes_clear()
for i in range(2, 4):
    firm_codes_list = firm_info.index ; option = i
    firm_f = get_all_firms_data(firm_codes_list, option)
    total_df = merge_two_dataframe(firm_info, firm_f, "firm_sheets" + "-" + str(option) + ".csv" )
