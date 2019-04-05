import os, json
import logging
import datetime as dt
from FinMind.Data import Load

from src.file import ensure_dir_path


with open("./config.json") as f:
    config = json.load(f)


def Buckup_dataset(dataset_name, TaiwanStockInfo):

    logger = logging.getLogger("{}".format(dataset_name))
    st = dt.datetime.now()

    if dataset_name == "TaiwanStockInfo":
        
        TaiwanStockInfo = Load.FinData(dataset=dataset_name)
        file_path = os.path.join(config["DirPath"]["BuckupRoot"], config["FilePath"][dataset_name])
        ensure_dir_path(file_path)
        TaiwanStockInfo.to_csv(file_path, index=False, encoding="utf_8_sig")

    elif dataset_name in ["TaiwanStockPrice", "InstitutionalInvestorsBuySell", "TaiwanStockStockDividend"]:

        for industry_category in TaiwanStockInfo["industry_category"].unique():
            logger.info("Buckup {} {}".format(dataset_name, industry_category))

            stock_id_list = TaiwanStockInfo[TaiwanStockInfo["industry_category"] == industry_category]["stock_id"].tolist()
            stock_data = Load.FinData(dataset=dataset_name, select=stock_id_list)
            file_path = os.path.join(config["DirPath"]["BuckupRoot"], 
                config["DirPath"][dataset_name], industry_category + ".csv")
            ensure_dir_path(file_path)
            stock_data.to_csv(file_path, index=False, encoding="utf_8_sig")

    else:
        logger.error("Do not have dataset:{}".format(dataset_name))
        exit(0)

    td = dt.datetime.now() - st
    logger.debug("Buckup {} data...Spending time={}!".format(dataset_name, td))

    return TaiwanStockInfo
