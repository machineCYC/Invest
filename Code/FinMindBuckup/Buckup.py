import os, json
import logging
import datetime as dt
import threading
import queue

from FinMind.Data import Load
from src.file import ensure_dir_path
from src.threadControler import launch_thread

with open("./config.json") as f:
    config = json.load(f)

def _save_data(dataset_name, stock_id, save_dir):
    logger = logging.getLogger("{}".format(dataset_name))

    st = dt.datetime.now()
    data = Load.FinData(dataset=dataset_name, select=[stock_id])
    file_path = os.path.join(save_dir, stock_id + '.csv')
    data.to_csv(file_path, index=False, encoding="utf_8_sig")

    td = dt.datetime.now() - st
    logger.info("Buckup {0}, Stock ID: {1}...Spending time={2}".format(dataset_name, stock_id, td))

def get_FinMindData(TaiwanStockInfo, dataset_name):
    que = queue.Queue()
    queLock = threading.Lock()

    for stock_id in TaiwanStockInfo['stock_id'].unique()[:10]:
        save_dir = config['DirPath']['BuckupRoot'] + config['DirPath']['TaiwanStockPrice']
        que.put(_save_data(dataset_name, stock_id, save_dir))

    launch_thread(que, queLock, 10)

def Buckup_dataset(dataset_name, TaiwanStockInfo):

    logger = logging.getLogger("{}".format(dataset_name))
    st = dt.datetime.now()

    if dataset_name == "TaiwanStockInfo":

        TaiwanStockInfo = Load.FinData(dataset=dataset_name)
        file_path = os.path.join(config["DirPath"]["BuckupRoot"], config["FilePath"][dataset_name])
        ensure_dir_path(file_path)
        TaiwanStockInfo.to_csv(file_path, index=False, encoding="utf_8_sig")

    elif dataset_name in ["TaiwanStockPrice", "InstitutionalInvestorsBuySell", "TaiwanStockStockDividend"]:

        # get_FinMindData(TaiwanStockInfo, dataset_name)
        for index, stock_id in enumerate(TaiwanStockInfo["stock_id"].unique()):
            logger.info("Buckup {0}, Index: {1}, Stock ID: {2}".format(dataset_name, index, stock_id))

            stock_data = Load.FinData(dataset=dataset_name, select=[stock_id])
            file_path = os.path.join(config["DirPath"]["BuckupRoot"],
                config["DirPath"][dataset_name], stock_id + ".csv")
            ensure_dir_path(file_path)
            stock_data.to_csv(file_path, index=False, encoding="utf_8_sig")

    else:
        logger.error("Do not have dataset:{}".format(dataset_name))
        exit(0)

    td = dt.datetime.now() - st
    logger.debug("Buckup {} data...Spending time={}!".format(dataset_name, td))

    return TaiwanStockInfo
