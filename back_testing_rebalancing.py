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

def get_strategy_date(start_date):
    temp_year = int(start_date.split('/')[0])
    temp_month = start_date.split('/')[1]
    if temp_month in '01 02 03 04 05'.split(' '):
        strategy_date = str(temp_year - 2) + '/12'
    else:
        strategy_date = str(temp_year - 1) + '/12'
    return strategy_date

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

def backtest_re(strategy, start_date, end_date, initial_money,
                price_df, fr_df, fs_df, invest_df, num,
                value_type=None, value_list=None, data_range=None):

    start_year = int(start_date.split('/')[0])
    end_year = int(end_date.split('/')[0])
    total_df = 0

    for temp in range(start_year, end_year):
        this_term_start = str(temp) + '/' + start_date.split('/')[1] # ex 2017-06
        this_term_end = str(temp+1) + '/' + start_date.split('/')[1] # ex 2018-06
        stretagy_date = get_strategy_date(this_term_start) # if 2017/06 -> return 2016/12

        if strategy.__name__ == 'high_roa':
            selected_fr_df = no_nan_firm_code(price_df, fr_df,
                                                  this_term_start)
            st_df = strategy(selected_fr_df, stretagy_date, num)

        elif strategy.__name__ == 'magic_formula':
            selected_invest_df = no_nan_firm_code(price_df, invest_df,
                                                  this_term_start)
            selected_fr_df = no_nan_firm_code(price_df, fr_df,
                                                  this_term_start)
            st_df = strategy(selected_fr_df,
                             selected_invest_df,
                             stretagy_date, num)

        elif strategy.__name__ == 'get_value_rank':
            selected_invest_df = no_nan_firm_code(price_df, invest_df,
                                                  this_term_start)
            st_df = strategy(selected_invest_df, value_type, stretagy_date, num)

        elif strategy.__name__ == 'make_value_combo':
            selected_invest_df = no_nan_firm_code(price_df, invest_df,
                                                  this_term_start)
            st_df = strategy(selected_invest_df, value_list, stretagy_date, num)

        elif strategy.__name__ == 'f_score_01':
            selected_fs_df = no_nan_firm_code(price_df, fs_df,
                                              this_term_start)
            st_df = strategy(selected_fs_df, stretagy_date, num)

        elif strategy.__name__ == 'get_value_quality':
            selected_invest_df = no_nan_firm_code(price_df, invest_df,
                                                  this_term_start)
            selected_fs_df = no_nan_firm_code(price_df, fs_df,
                                              this_term_start)
            st_df = strategy(selected_invest_df, selected_fs_df, stretagy_date, num)

        elif strategy.__name__ == 'get_momentum_rank':
            index_date = price_df[this_term_start].index[0]
            st_df = strategy(price_df, index_date, data_range, num)

        backtest = back_test_beta(price_df, st_df,
                                  this_term_start, this_term_end,
                                  initial_money)
        temp_end = backtest[this_term_end].index[0]
        backtest = backtest[:temp_end]
        initial_money = backtest['종합포트폴리오'][-1]

        if temp == start_year:
            total_df = backtest
        else:
            total_df = pd.concat([total_df[:-1], backtest])

    total_df['일변화율'] = (total_df['종합포트폴리오'].pct_change()) * 100
    total_df['총변화율'] = (total_df['종합포트폴리오']\
                                 /total_df['종합포트폴리오'][0]-1) * 100
    return total_df



''' Load Data '''
fs_df = sf.read_fundamental_csv("csv_file/firm_data-1.csv")
fr_df = sf.read_fundamental_csv("csv_file/firm_data-2.csv")
invest_df = sf.read_fundamental_csv("csv_file/firm_data-3.csv")
price_df = st.read_price_csv("csv_file/price_data.csv")

''' Set Back Testing Rebalancing Parameters'''
strategy = sf.get_value_rank
# strategy = st.get_momentum_rank
start_date = "2017/06"
end_date = "2019/06"
initial_money = 100000000
value_type = "PER"
value_list = ["PER", "PBR", "PSR"]
data_range = 250

result1 = backtest_re(strategy, start_date, end_date, initial_money,
                      price_df, fr_df, fs_df, invest_df, 20,
                      value_type=value_type, value_list=value_list,
                      data_range=data_range)

print(result1)
