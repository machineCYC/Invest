import os, csv
import os
import json
import numpy as np
import pandas as pd 

from src.data import deleteComma


with open("config.json") as f:
    config = json.load(f)

file_path = os.path.join(config["Raw"]["DataRoot"], config["Raw"]["Stock"])
with open(file_path, "r", encoding="ISO-8859-1") as stock:
    df_stock = pd.read_csv(stock)

cm = df_stock["代碼"].drop_duplicates() # 1684

# deal data type
df_stock[["代碼", "中文簡稱"]] = df_stock[["代碼", "中文簡稱"]].astype(str)
df_stock["中文簡稱"] = df_stock["中文簡稱"].apply(lambda x: x.strip())
df_stock["日期"] = pd.to_datetime(df_stock["日期"], format="%Y%m%d")
df_stock["YEAR"] = df_stock["日期"].dt.year
df_stock["MONTH"] = df_stock["日期"].dt.month
df_stock["DAY"] = df_stock["日期"].dt.day

df_stock["開盤價(元)"] = df_stock["開盤價(元)"].apply(deleteComma)
df_stock["最高價(元)"] = df_stock["最高價(元)"].apply(deleteComma)
df_stock["最低價(元)"] = df_stock["最低價(元)"].apply(deleteComma)
df_stock["收盤價(元)"] = df_stock["收盤價(元)"].apply(deleteComma)
df_stock["成交張數(張)"] = df_stock["成交張數(張)"].apply(deleteComma)

df_stock[["開盤價(元)", "最高價(元)", "最低價(元)", "收盤價(元)", "成交張數(張)"]] = df_stock[["開盤價(元)", "最高價(元)", "最低價(元)", "收盤價(元)", "成交張數(張)"]].apply(pd.to_numeric)

# rename
columns = {
    "代碼":"CMCODEID", "中文簡稱":"CMCODENM", "日期":"DATE", 
    "開盤價(元)":"OPEN", "最高價(元)":"HIGH", "最低價(元)":"LOW", "收盤價(元)":"CLOSE", 
    "成交張數(張)":"VOLUME"}
df_stock = df_stock.rename(index=str, columns=columns)

file_path = os.path.join(config["DM"]["DataRoot"], config["DM"]["Stock"])
df_stock.to_csv(file_path, encoding="utf-8", index=False)