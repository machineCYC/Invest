import os
import requests
import json
import time
import csv

from collections import namedtuple


with open("./config.json") as f:
    config = json.load(f)
# date, Trading_Volume, Trading_money, open, max, min, close, spread, Trading_turnover, stock_id
# ["日期", "成交股數", "成交金額", "開盤價", "最高價", "最低價", "收盤價", "漲跌價差", "成交筆數"]
DATATUPLE = namedtuple("Data", 
    ["date", "capacity", "turnover", "open", "high", "low", "close", "change", "transaction"])


def catch_stock_data(year, month, stock_id):
    param = {"date": "{:d}{:02d}01".format(year, month) , "stockNo": stock_id}
    headers = {
        'Accept-Language': 'zh-TW', 
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
    }

    url_twse_base = "http://www.twse.com.tw/"
    url_source = os.path.join(url_twse_base, "exchangeReport/STOCK_DAY")
    res = requests.get(url_source, param, headers=headers)
    time.sleep(5)

    s = json.loads(res.text)
    
    if s["stat"] == "OK":
        data = _convert(s)
    else:
        data = []

    return data


def _standard_data(data):
    data[0] = data[0]
    data[1] = int(data[1].replace(",", ""))
    data[2] = int(data[2].replace(",", ""))
    data[3] = None if data[3] == "--" else float(data[3].replace(",", ""))
    data[4] = None if data[4] == "--" else float(data[4].replace(",", ""))
    data[5] = None if data[5] == "--" else float(data[5].replace(",", ""))
    data[6] = None if data[6] == "--" else float(data[6].replace(",", ""))
    data[7] = float(0.0 if data[7].replace(",", "") == "X0.00" else data[7].replace(",", ""))
    data[8] = int(data[8].replace(",", ""))
    return DATATUPLE(*data)

def _convert(data):
    result = [_standard_data(d) for d in data["data"]]
    return result

def save_csv(data, stock_id):
    file_path = os.path.join(
        config["DirPath"]["BuckupRoot"], config["DirPath"]["TaiwanStockPrice"], stock_id + ".csv")
    
    outputFile = open(file_path, "w", newline="")
    outputWriter = csv.writer(outputFile)
    head = DATATUPLE(*data[0]._fields)
    outputWriter.writerow(head)
    for d in data:
        outputWriter.writerow(d)

    outputFile.close()