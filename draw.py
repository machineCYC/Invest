import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams["axes.grid"] = True
plt.rcParams["legend.fontsize"] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams["font.sans-serif"]=["SimHei"] #用来正常显示中文标签 

with open("config.json") as f:
    config = json.load(f)

file_path = os.path.join(config["DM"]["DataRoot"], config["DM"]["Stock"])
stock = pd.read_csv(file_path, encoding="utf-8")
# stock["DATE"] = pd.to_datetime(stock["DATE"], format="%Y%m%d")

def drawPricePath(df):

    cm_id = df["CMCODEID"].values[0]
    cm_nm = df["CMCODENM"].values[0]
    start_date = df["DATE"].values[0]
    end_date = df["DATE"].values[-1]

    fig = plt.figure(num=1, figsize=(30, 15), facecolor=".6")
    axes = fig.add_subplot(111)

    price = df["CLOSE"].values
    date_List = df["DATE"].values
    vol = df["VOLUME"].values

    ind = np.arange(0, len(date_List))
    ind_pds = pd.DataFrame(np.array([date_List, ind]).T, columns=list(["date","x_pos"]))
    ind_pds["x_pos"] = pd.to_numeric(ind_pds["x_pos"])
    xpos_pds = pd.DataFrame(np.array([ind, np.repeat(1, len(date_List))]).T, columns=list(["x_pos","hasData"]))
    xpos = pd.merge(ind_pds, xpos_pds)["x_pos"].values

    axes.plot(xpos, price, lw=2, c="b", label=str(cm_id)+cm_nm, marker="o")
    axes.set_xticks(np.arange(0, len(date_List), int(np.ceil(len(date_List) / 150)))+0.1)
    date_List = date_List[np.arange(0, len(date_List), int(np.ceil(len(date_List) / 150)))]
    axes.set_xticklabels(date_List, rotation=90)
    axes.legend()

    axes2 = axes.twinx()
    axes2.bar(xpos, vol, color="r", label="VOLUME", alpha=0.3)
    axes2.set_yticks(np.arange(0, 400000, 20000))
    axes2.set_yticklabels(np.arange(0, 400000, 20000))
    axes2.grid(False)
    axes2.tick_params(colors="r")

    fig.tight_layout()
    Plotname = "[" + str(cm_id) + cm_nm + "]" + str(start_date) + "_" + str(end_date) + ".png"
    file_folder = config["PLOT"]["OutputRoot"]
    if not os.path.isdir(file_folder):
        os.mkdir(file_folder)
    file_path = os.path.join(file_folder, Plotname)
    fig.savefig(file_path, bbox_inches="tight")
    plt.close(fig)

start_y = 2018
start_m = 3
start_d = 1
stock2303 = stock[(stock["CMCODEID"]==2303) & 
    ((stock["YEAR"] > start_y) | ((stock["YEAR"] == start_y) & (stock["MONTH"] >= start_m) & ((stock["DAY"] >= start_d))))]

cm_list = [
    2330, 2002, 2317, 2412, 2357
    2303, 5871, 2353,
    2891, 2834, 2886, 2881, 2884, 2882, 
    3558]
for cm in cm_list:
    df = stock[(stock["CMCODEID"]==cm)]
    drawPricePath(df)
