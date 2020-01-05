import pandas as pd
import numpy as np
pd.set_option('display.unicode.east_asian_width', True)

''' read csv file '''
def read_fundamental_csv(path):
    df = pd.read_csv(path, index_col=["Unnamed: 0"], dtype='unicode')
    big_col = list(df.columns)
    small_col = list(df.iloc[0])

    new_big_col = []
    for num, col in enumerate(big_col):
        new_big_col.append(col[:7])

    df.columns = [new_big_col, small_col]
    df = df.loc[df.index.dropna()]
    return df

def check_IFRS(x):
    if x == 'N/A(IFRS)':
        return np.NaN
    else:
        return x

''' find low_per '''
def low_per(invest_df, index_date, num):
    invest_df[(index_date, 'PER')] = pd.to_numeric(
                                            invest_df[(index_date, 'PER')])
    per_sorted = invest_df.sort_values(by=(index_date, 'PER'))
    return per_sorted[index_date][:num]

''' find high_roa '''
def high_roa(fr_df, index_date, num):
    fr_df[(index_date, 'ROA')] = fr_df[(index_date, 'ROA')].apply(check_IFRS)
    fr_df[(index_date, 'ROA')] = pd.to_numeric(
                                            fr_df[(index_date, 'ROA')])
    roa_sorted = fr_df.sort_values(by=(index_date, 'ROA'), ascending=False)
    return roa_sorted[index_date][:num]

''' this magic formula is standard for low per and high roa '''
def magic_formula(fr_df, invest_df, index_date, num):
    per = low_per(invest_df, index_date, None)
    roa = high_roa(fr_df, index_date, None)
    per['per_rank'] = per['PER'].rank()
    roa['roa_rank'] = roa['ROA'].rank(ascending=False)
    magic = pd.merge(per, roa, how='outer', left_index=True, right_index=True)
    magic['magic_rank'] = (magic['per_rank'] + magic['roa_rank'])
    magic['magic_rank'] = magic['magic_rank'].rank().sort_values()
    magic = magic.sort_values(by='magic_rank')
    return magic

''' low PER, PBR, PSR, PCE '''
def get_value_rank(invest_df, value_type, index_date, num):
    invest_df[(index_date, value_type)] = pd.to_numeric(
                                            invest_df[(index_date, value_type)])
    value_sorted = invest_df.sort_values(by=(index_date, value_type))
    value_sorted = value_sorted[index_date]

    value_sorted[value_type+'_rank'] = value_sorted[value_type].rank()
    return value_sorted[[value_type, value_type+'_rank']][:num]

def make_value_combo(invest_df, value_list, index_date, num):
    for i, value in enumerate(value_list):
        temp_df = get_value_rank(invest_df, value, index_date, None)
        if i == 0:
            value_combo_df = temp_df
            rank_combo = temp_df[value+'_rank']
        else:
            value_combo_df = pd.merge(value_combo_df, temp_df, how='outer',
                                      left_index=True, right_index=True)
            rank_combo = rank_combo + temp_df[value+'_rank']
    value_combo_df['all_rank'] = rank_combo.rank()
    value_combo_df = value_combo_df.sort_values(by='all_rank')
    return value_combo_df[:num]

''' F-Score '''
def make_numeric(score_list, fs_df, index_date):
    fs_df[(index_date, score_list)] = pd.to_numeric(
                                            fs_df[(index_date, score_list)])
    return fs_df[(index_date, score_list)]

def f_score_01(fs_df, index_date, num):
    score_lists = ["당기순이익", "영업활동으로인한현금흐름"]
    for i, score_list in enumerate(score_lists):
        fs_df[(index_date, score_list)] = make_numeric(score_list,
                                                            fs_df,
                                                            index_date)
    fscore_df = fs_df.loc[:, index_date].fillna(0)
    fscore_df.loc[fscore_df['당기순이익'] > 0, "당기순이익점수"] = 1
    fscore_df.loc[fscore_df['영업활동으로인한현금흐름'] > 0, "영업활동점수"] = 1
    condition = fscore_df['영업활동으로인한현금흐름'] > fscore_df['당기순이익']
    fscore_df.loc[condition, "더큰영업활동점수"] = 1

    all_score_list = ["당기순이익점수", "영업활동점수", "더큰영업활동점수"]
    fscore_df["종합점수"] = fscore_df[all_score_list].sum(axis=1)
    fscore_df = fscore_df[fscore_df["종합점수"] == 3]
    return fscore_df

''' value + quality '''
def get_value_quality(invest_df, fs_df, index_date, num):
    value_list = ["PER", "PBR", "PSR", "PCR"]
    value = make_value_combo(invest_df, value_list, index_date, None)
    quality  = f_score_01(fs_df, index_date, None)
    value_quality = pd.merge(value, quality, how='outer',
                             left_index=True, right_index=True)
    value_quality_filtered = value_quality[value_quality['종합점수'] == 3]
    vq_df = value_quality_filtered.sort_values(by='all_rank')
    return vq_df[:num]


if __name__ == "__main__":
    ''' Load Data '''
    fs_path = "csv_file/firm_data-1.csv"
    fr_path = "csv_file/firm_data-2.csv"
    invest_path = "csv_file/firm_data-3.csv"

    fs_df = read_fundamental_csv(fs_path)
    fr_df = read_fundamental_csv(fr_path)
    invest_df = read_fundamental_csv(invest_path)

    ''' Magic Formula '''
    index_date = '2016/12'
    low_per_df = low_per(invest_df, index_date, None)
    high_roa_df = high_roa(fr_df, index_date, None)
    df = magic_formula(fr_df, invest_df, index_date, None)
    print(df)

    ''' low PER, PBR, PSR, PCE, value combo '''
    # index_date = '2018/12'
    # value_list = ["PER", "PBR", "PSR", "PCR"]
    # df = make_value_combo(invest_df, value_list,  index_date, 10)
    # print(df)

    ''' F-Score '''
    # index_date = '2016/12'
    # df = f_score_01(fs_df, index_date, 6)
    # print(df)

    ''' value + quality '''
    # index_date = '2018/12'
    # df = get_value_quality(invest_df, fs_df, index_date, 20)
    # print(df['all_rank'])
