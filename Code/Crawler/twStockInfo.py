# Usage: Download all stock code info from TWSE
#
# TWSE equities = 上市證券
# TPEx equities = 上櫃證券
#

import os
import csv
import json
import requests

from collections import namedtuple
from lxml import etree


with open('./config.json') as f:
    config = json.load(f)

TWSE_EQUITIES_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
TPEX_EQUITIES_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
ROW = namedtuple('Row', ['type', 'code', 'name', 'ISIN', 'start', 'market', 'group', 'CFI'])


def make_row_tuple(typ, row):
    code, name = row[1].split('\u3000')
    return ROW(typ, code, name, *row[2: -1])


def fetch_data(url):
    r = requests.get(url)
    root = etree.HTML(r.text)
    trs = root.xpath('//tr')[1:]

    result = []
    typ = ''
    for tr in trs:
        tr = list(map(lambda x: x.text, tr.iter()))
        if len(tr) == 4:
            # This is type
            typ = tr[2].strip(' ')
        else:
            # This is the row data
            result.append(make_row_tuple(typ, tr))
    return result


def to_csv(url, path):
    data = fetch_data(url)
    with open(path, 'w', newline='', encoding='utf_8') as csvfile:
        writer = csv.writer(csvfile,
                            delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data[0]._fields)
        for d in data:
            writer.writerow([_ for _ in d])


if __name__ == '__main__':
    to_csv(TWSE_EQUITIES_URL, os.path.join(config["DirPath"]["BuckupRoot"], config["FilePath"]["twse_equities"]))
    to_csv(TPEX_EQUITIES_URL, os.path.join(config["DirPath"]["BuckupRoot"], config["FilePath"]["tpex_equities"]))
