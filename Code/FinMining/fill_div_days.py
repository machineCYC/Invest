'''
A script will calculate days that fill dividend in this year,
if not fill dividend in this year will return -1
'''
import os
import json
import argparse
import numpy as np
import pandas as pd
import datetime

from src.Loader import get_data

with open("./config.json") as f:
    config = json.load(f)

def _filter_data(df):
    if not df[~df['Ex_dividend_transaction_day'].isnull()].empty:
        index = df[~df['Ex_dividend_transaction_day'].isnull()].index[0] - 1
        tmp_df = df[df.index>=index]
    else:
        tmp_df = pd.DataFrame(columns=df.columns)
    return tmp_df

def _cal_fill_div_day(price_list):
    original_price = price_list[0]
    for i, s in enumerate(price_list[1:]):
        if s >= original_price:
            return i
    return -1

def cal_stock_fill_div_days(stock_id):
    div_data = get_data(
        dataset_name='TaiwanStockStockDividend', stock_id=[stock_id])

    price_data =  get_data(
        dataset_name='TaiwanStockPrice', stock_id=[stock_id])

    if not (price_data.empty or div_data.empty):
        div_data['year'] = div_data['date'].map(lambda x: x.split('-')[0])
        price_data['year'] = price_data['date'].map(lambda x: x.split('-')[0])

        mge = pd.merge(
            price_data[['date', 'year','stock_id', 'close']],
            div_data[['stock_id','Ex_dividend_transaction_day']],
            left_on=['date', 'stock_id'], right_on=['Ex_dividend_transaction_day', 'stock_id'], how='left')

        mge_gby = mge.groupby(['stock_id', 'year'], as_index=False).apply(_filter_data).reset_index(drop=True)
        mge_gby = mge_gby.groupby(['stock_id', 'year'], as_index=False).agg({'close': lambda x: list(x)})

        mge_gby['fill_days'] = mge_gby['close'].map(lambda x: _cal_fill_div_day(x))
        return mge_gby[['stock_id', 'year', 'fill_days']]
    else:
        return pd.DataFrame(columns=['stock_id', 'year', 'fill_days'])

def main(args):
    result = []
    for stock_id in args.stock_id_list:
        print('Process stock:{}'.format(stock_id))
        stock_fill_day = cal_stock_fill_div_days(stock_id)
        result.append(stock_fill_day)

    result = pd.concat(result, axis=0)
    result.to_csv(os.path.join(config['DirPath']['ReportData'], 'stock_fill_div_days.csv'), index=False)

if __name__ == '__main__':
    stock_id_list = ['2002', '2891', '2881', '2884', '2882', '2887', '2886', '5880', '2834']
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stock_id_list",
        type=str,
        default=stock_id_list,
        help="A list of stock id to calculate fill div days"
    )
    main(parser.parse_args())