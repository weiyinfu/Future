"""
一份mock的数据
"""
from os.path import *

import pandas as pd

cur = dirname(abspath(__file__))


def load(filename: str):
    a = pd.read_csv(filename, encoding="gbk")
    a = a.rename(
        columns={
            "开盘价": "Open",
            "收盘价": "Close",
            "最高价": "High",
            "最低价": "Low",
            "//时间": "Date",
            "myboll:UpLine": "Up",
            "myboll:DownLine": "Down",
            "myboll:MidLine": "Mid",
            "成交量": "Volume",
        }
    )
    data = {
        "x": a["Date"].values.tolist(),
        "y": a.loc[:, ("Open", "Close", "Low", "High")].values.tolist(),  # k线五元组
        "up": a["Up"].values.tolist(),
        "down": a["Down"].values.tolist(),
        "mid": a["Mid"].values.tolist(),
    }
    return data


myboll = load(join(cur, "../myboll.csv"))
