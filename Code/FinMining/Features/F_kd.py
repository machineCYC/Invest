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
    need_col = ['stock_id', 'date', 'max', 'min', 'close']
    tecAnalysis = analysis.TecAnalysis()
    smoothing = analysis.Smoothing()
    for file_path in target_file:
        data = pd.read_csv(file_path, encoding='utf-8')[need_col]
        data['MMax9'] = smoothing.moving_max(data['max'].values, days=9)
        data['MMin9'] = smoothing.moving_min(data['min'].values, days=9)
        data['RSV'] = round((data['close'] - data['MMin9']) / (data['MMax9'] - data['MMin9']) * 100, 2)
        data['K9'], data['D9'] = tecAnalysis.cal_kd_value(data['RSV'].values)
        data = data.drop(['max', 'min', 'MMax9', 'MMin9', 'RSV'], axis=1)
        if not os.path.exists(save_file_dir):
            os.mkdir(save_file_dir)
        data.to_csv(os.path.join(save_file_dir, 'F_kd_' + os.path.basename(file_path)), index=False)

if __name__ == '__main__':
    main()