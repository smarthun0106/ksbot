import stretagies_fundamental as sf
import stretagies_technical as st
import pandas as pd
import matplotlib.pyplot as plt

def remove_A(firm_codes):
    code_list = []
    for firm_code in firm_codes:
        code_list.append(firm_code.replace('A', ''))
    return code_list

def no_nan_firm_code(price_df, data_df, standard_date):
    new_code_list = []
    for code in price_df[standard_date].iloc[0].dropna().index:
        new_code_list.append('A' + code)
    selected_df = data_df.loc[new_code_list]
    return selected_df

def back_test_beta(price_df, stretagy_df,
                   start_date, end_date, initial_money):
    # Preprocessing
    low_pbr_code_list = remove_A(stretagy_df.index)
    low_pbr_price = price_df[low_pbr_code_list][start_date:]

    # portfolio stock number,
    # key : which firm_code,
    # value : how many shares you could buy with your assets
    pf_stock_num = {}
    stock_amount = 0
    each_money = initial_money / stretagy_df.shape[0]
    for firm_code in low_pbr_price.columns:
         temp = int(each_money / low_pbr_price[firm_code][0])
         pf_stock_num[firm_code] = temp
         stock_amount = stock_amount + temp * low_pbr_price[firm_code][0]
    cash_amount = initial_money - stock_amount

    # stock portfolio
    # you can see the money flow
    stock_pf = 0
    for firm_code in low_pbr_price.columns:
        stock_pf = stock_pf + low_pbr_price[firm_code] * pf_stock_num[firm_code]

    # make portfolio
    low_pbr_backtest = pd.DataFrame({'주식포트폴리오':stock_pf[:end_date]})
    low_pbr_backtest.loc[:, '현금포트폴리오'] = cash_amount
    low_pbr_backtest['종합포트폴리오'] = low_pbr_backtest['주식포트폴리오'] + \
                                                low_pbr_backtest['현금포트폴리오']
    low_pbr_backtest['일변화율'] = (low_pbr_backtest['종합포트폴리오'].pct_change())*100
    low_pbr_backtest['총변화율'] = (low_pbr_backtest['종합포트폴리오']/initial_money - 1)*100
    return low_pbr_backtest


''' Load Data '''
invest_df = sf.read_fundamental_csv("csv_file/firm_data-3.csv")
fs_df = sf.read_fundamental_csv("csv_file/firm_data-1.csv")
price_df = st.read_price_csv("csv_file/price_data.csv")

''' Set Back Testing Parameters'''
standard_date = "2016/12" ; start_date = "2017/06" ; end_date = "2018/5"
initial_money = 50000000
print(get_stratrage_date(start_date))

''' Back Testing '''
selected_invest_df = no_nan_firm_code(price_df, fs_df, standard_date)

# # low per
# low_per = sf.get_value_rank(selected_invest_df, "PER", standard_date, 20)
# low_per_df = back_test_beta(price_df, low_per,
#                            start_date, end_date, initial_money)
#
# # low pbr
# low_pbr = sf.get_value_rank(selected_invest_df, "PBR", standard_date, 20)
# low_pbr = low_pbr.dropna()
# low_pbr_df = back_test_beta(price_df, low_pbr,
#                            start_date, end_date, initial_money)

# # Interval PBR
# low_pbr = sf.get_value_rank(selected_invest_df, "PBR", standard_date, None)
# low_pbr = low_pbr.dropna()
# length = int(len(low_pbr)/5)
# low_pbr_df1 = back_test_beta(price_df, low_pbr[:length],
#                            start_date, end_date, initial_money)
#
# low_pbr_df2 = back_test_beta(price_df, low_pbr[length:length*2],
#                            start_date, end_date, initial_money)
#
# low_pbr_df3 = back_test_beta(price_df, low_pbr[length*2:length*3],
#                            start_date, end_date, initial_money)
#
# low_pbr_df4 = back_test_beta(price_df, low_pbr[length*3:length*4],
#                            start_date, end_date, initial_money)
#
# low_pbr_df5 = back_test_beta(price_df, low_pbr[length*4:length*5],
#                            start_date, end_date, initial_money)

f_score_result = sf.f_score_01(selected_invest_df, standard_date, 20)
f_score_df = back_test_beta(price_df, f_score_result,
                           start_date, end_date, initial_money)

''' Visualization '''
# PBR Visualization
feature = '총변화율'
# plt.figure(figsize=(12, 7))
# low_pbr_df1[feature].plot(label='PBR1')
# low_pbr_df2[feature].plot(label='PBR2')
# low_pbr_df3[feature].plot(label='PBR3')
# low_pbr_df4[feature].plot(label='PBR4')
# low_pbr_df5[feature].plot(label='PBR5')
# plt.legend()
# plt.show()

# # F-score
# plt.figure(figsize=(12, 7))
# f_score_df[feature].plot()
# plt.show()
