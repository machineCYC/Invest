import os, json
import logging
import datetime

mpl_logger = logging.getLogger("matplotlib") 
mpl_logger.setLevel(logging.WARNING)


with open("./config.json") as f:
    config = json.load(f)


# 基礎設定
log_filename = datetime.datetime.now().strftime("./log/%Y-%m-%d_%H_%M_%S.log")
loglevel = getattr(logging, config["Logging"]["Level"])
logging.basicConfig(level=loglevel,
                    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                    datefmt="%m-%d %H:%M",
                    # filename=log_filename,
                    handlers = [logging.FileHandler(log_filename, "w", "utf-8"),])
 
# 定義 handler 輸出 sys.stderr
console = logging.StreamHandler()
console.setLevel(loglevel)
# 設定輸出格式
formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
# handler 設定輸出格式
console.setFormatter(formatter)
# 加入 hander 到 root logger
logging.getLogger("").addHandler(console)

logger_FlowControl = logging.getLogger("FinMindDataBuckupFlow")

logger_FlowControl.info("FinMind data buckup")