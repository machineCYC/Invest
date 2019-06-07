import os
import time
import json
import datetime
import pandas as pd

from src.catch import catch_stock_data, save_csv


with open("./config.json") as f:
    config = json.load(f)

file_path = os.path.join(config["DirPath"]["BuckupRoot"], config["FilePath"]["twse_equities"])
twse_equities = pd.read_csv(file_path, encoding='utf-8')
file_path = os.path.join(config["DirPath"]["BuckupRoot"], config["FilePath"]["tpex_equities"])
tpex_equities = pd.read_csv(file_path, encoding='utf-8')

stock_id_list = twse_equities['code'].values.tolist()
stock_start_list = twse_equities['start'].values.tolist()

stock_id  = "2303"
# stock_start = '1985/07/16'
stock_start = '2000/07/16'
start_year = int(stock_start.split("/")[0])
start_month = int(stock_start.split("/")[1])

current_time = datetime.datetime.now()
current_year = current_time.year
current_month = current_time.month

# data = catch_stock_data(2000, month, stock_id)

df = []
for year in range(start_year, current_year+1, 1):
    month_start = 1
    month_end = 13
    if year == current_year:
        month_end = current_month
    elif year == start_year:
        month_start = start_month

    for month in range(month_start, month_end+1, 1):
        data = catch_stock_data(year, month, stock_id)
        df.extend(data)

save_csv(df, stock_id)
