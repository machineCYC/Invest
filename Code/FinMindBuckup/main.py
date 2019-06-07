import os
import time
import pandas as pd

from config_init import config, logger_FlowControl
from FinMindBuckup.Buckup import Buckup_dataset

logger_FlowControl.info("FinMind data buckup")

time1 = time.time()
"""
TaiwanStockInfo
股票總表
"""
if (config["StepControl"]["Step_TaiwanStockInfo"]=="ON"):
    logger_FlowControl.info("Start Buckup TaiwanStockInfo data")

    TaiwanStockInfo = Buckup_dataset(dataset_name="TaiwanStockInfo", TaiwanStockInfo=None)

    logger_FlowControl.info("Finish Buckup TaiwanStockInfo data")
else:
    logger_FlowControl.info("Skip Buckup TaiwanStockInfo data")

    file_path = os.path.join(config["DirPath"]["BuckupRoot"], config["FilePath"]["TaiwanStockInfo"])
    TaiwanStockInfo = pd.read_csv(file_path, encoding="utf_8_sig")

time2 = time.time()
logger_FlowControl.info("%s function took %0.3f ms" % ("STEP1", (time2 - time1) * 1000.0))

"""
TaiwanStockPrice
股價資訊
"""
if (config["StepControl"]["Step_TaiwanStockPrice"]=="ON"):
    logger_FlowControl.info("Start Buckup TaiwanStockPrice data")

    _ = Buckup_dataset(dataset_name="TaiwanStockPrice", TaiwanStockInfo=TaiwanStockInfo)

    logger_FlowControl.info("Finish Buckup TaiwanStockPrice data")
else:
    logger_FlowControl.info("Skip Buckup TaiwanStockPrice data")

"""
InstitutionalInvestorsBuySell
股票外資買賣資訊
"""
if (config["StepControl"]["Step_InstitutionalInvestorsBuySell"]=="ON"):
    logger_FlowControl.info("Start Buckup InstitutionalInvestorsBuySell data")

    _ = Buckup_dataset(dataset_name="InstitutionalInvestorsBuySell", TaiwanStockInfo=TaiwanStockInfo)

    logger_FlowControl.info("Finish Buckup InstitutionalInvestorsBuySell data")
else:
    logger_FlowControl.info("Skip Buckup InstitutionalInvestorsBuySell data")

"""
TaiwanStockStockDividend
股票股利資訊
"""
if (config["StepControl"]["Step_TaiwanStockStockDividend"]=="ON"):
    logger_FlowControl.info("Start Buckup TaiwanStockStockDividend data")

    _ = Buckup_dataset(dataset_name="TaiwanStockStockDividend", TaiwanStockInfo=TaiwanStockInfo)

    logger_FlowControl.info("Finish Buckup TaiwanStockStockDividend data")
else:
    logger_FlowControl.info("Skip Buckup TaiwanStockStockDividend data")
