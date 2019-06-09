'''
create macd features
'''
import os
import json
import numpy as np
import pandas as pd

from FinMining.src import analysis


with open("./config.json") as f:
    config = json.load(f)

target_file = ['0050.csv', '0056.csv', '^TWII.csv']
file_dir = os.path.join(config["DirPath"]["BuckupRoot"], config["DirPath"]["TaiwanStockPrice"])
target_file = [os.path.join(file_dir, f) for f in target_file]
save_file_dir = '../../data/Features/'


def main():
    need_col = ['stock_id', 'date', 'close']
    tecAnalysis = analysis.TecAnalysis()
    for file_path in target_file:
        data = pd.read_csv(file_path, encoding='utf-8')[need_col]
        data['ema12'] = tecAnalysis.moving_exp_means(data['close'].values, 12)
        data['ema26'] = tecAnalysis.moving_exp_means(data['close'].values, 26)
        data['dif'] = data['ema12'].values - data['ema26'].values
        data['macd'] = tecAnalysis.moving_exp_means(data['dif'].values, 9)
        data['osc'] = data['dif'].values - data['macd'].values
        data = data.drop(['ema12', 'ema26', 'dif'], axis=1)
        if not os.path.exists(save_file_dir):
            os.mkdir(save_file_dir)
        data.to_csv(os.path.join(save_file_dir, 'F_macd_' + os.path.basename(file_path)), index=False)

if __name__ == '__main__':
    main()