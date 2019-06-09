import os
import sys
import json
import numpy as np
import pandas as pd

from FinMining.src import analysis


with open("./config.json") as f:
    config = json.load(f)

target_file = ['0050.csv', '0056.csv', '^TWII.csv']
file_dir = os.path.join(config["DirPath"]["BuckupRoot"], config["DirPath"]["TaiwanStockPrice"])
target_file_path = [os.path.join(file_dir, f) for f in target_file]

target_file = ['^DJI.csv', '^GSPC.csv']
file_dir = os.path.join(config["DirPath"]["BuckupRoot"], config["DirPath"]["USStockPrice"])
target_file_path.extend([os.path.join(file_dir, f) for f in target_file])

save_file_dir = '../../data/Features'

def main():
    need_col = ['stock_id', 'date', 'close']
    smoothing = analysis.Smoothing()
    for file_path in target_file_path:
        data = pd.read_csv(file_path, encoding='utf-8')
        data.columns = map(str.lower, data.columns)
        data = data[need_col]
        data['MA20'] = smoothing.moving_means(data['close'].values, days=20)
        data['bias20'] = (data['close'].values - data['MA20'].values) / data['MA20'].values
        if not os.path.exists(save_file_dir):
            os.mkdir(save_file_dir)
        data.to_csv(os.path.join(save_file_dir, 'F_ma_' + os.path.basename(file_path)), index=False)

if __name__ == "__main__":
    main()