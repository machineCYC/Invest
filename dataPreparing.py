import os, csv
import json
import numpy as np
import pandas as pd 

from src.data import deleteComma


with open("config.json") as f:
    config = json.load(f)


def purify_data(df, save_path):
    cm = df["代碼"].drop_duplicates() # 1684

    # deal data type
    df[["代碼", "中文簡稱"]] = df[["代碼", "中文簡稱"]].astype(str)
    df["中文簡稱"] = df["中文簡稱"].apply(lambda x: x.strip())
    df["日期"] = pd.to_datetime(df["日期"], format="%Y%m%d")
    df["YEAR"] = df["日期"].dt.year
    df["MONTH"] = df["日期"].dt.month
    df["DAY"] = df["日期"].dt.day

    df["開盤價(元)"] = df["開盤價(元)"].apply(deleteComma)
    df["最高價(元)"] = df["最高價(元)"].apply(deleteComma)
    df["最低價(元)"] = df["最低價(元)"].apply(deleteComma)
    df["收盤價(元)"] = df["收盤價(元)"].apply(deleteComma)
    df["成交張數(張)"] = df["成交張數(張)"].apply(deleteComma)

    df[["開盤價(元)", "最高價(元)", "最低價(元)", "收盤價(元)", "成交張數(張)"]] = df[["開盤價(元)", "最高價(元)", "最低價(元)", "收盤價(元)", "成交張數(張)"]].apply(pd.to_numeric)

    # rename
    columns = {
        "代碼":"CMCODEID", "中文簡稱":"CMCODENM", "日期":"DATE", 
        "開盤價(元)":"OPEN", "最高價(元)":"HIGH", "最低價(元)":"LOW", "收盤價(元)":"CLOSE", 
        "成交張數(張)":"VOLUME"}
    df = df.rename(index=str, columns=columns)

    if not os.path.exists(config["DM"]["DataRoot"]):
        os.mkdir(config["DM"]["DataRoot"])
    file_path = os.path.join(config["DM"]["DataRoot"], save_path)
    df.to_csv(file_path, encoding="utf-8", index=False)

if __name__ == "__main__":
    file_path = os.path.join(config["Raw"]["DataRoot"], config["Raw"]["Stock"])
    with open(file_path, "r", encoding="big5-hkscs") as stock:
        df_stock = pd.read_csv(stock)

    purify_data(df_stock, config["DM"]["Stock"])

    file_path = os.path.join(config["Raw"]["DataRoot"], config["Raw"]["ETF"])
    with open(file_path, "r", encoding="big5-hkscs") as etf:
        df_stock = pd.read_csv(etf)

    purify_data(df_stock, config["DM"]["ETF"])