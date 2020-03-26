import numpy as np
import pandas as pd

a = pd.read_csv("./myboll.csv", encoding='gbk')
a = a.rename(columns={
    "开盘价": "Open",
    "收盘价": "Close",
    "最高价": "High",
    "最低价": "Low",
    "//时间": "Date",
    "myboll:UpLine": "Up",
    "myboll:DownLine": "Down",
    "myboll:MidLine": "Mid",
    "成交量": "Volume",
})
a['Date'] = [i.replace('/', '-') + ":00" for i in a['Date']]
a['Date'] = pd.DatetimeIndex(a['Date'])
a.index = a['Date']

Length = 60
Offset = 0.25
Uplines = []
DownLines = []
MidLines = []
Band = []
lots = []

for i in range(Length,len(a)-Length):
    beg = max(i - Length, 0)
    MidLine = np.mean(a[beg:i]['Close'])
    Band = np.std(a[beg:i]['Close'])
    Upline = MidLine + Offset * Band
    DownLine = MidLine - Offset * Band
    lots = 1
    MidLines.append(MidLine)
    Uplines.append(Upline)
    DownLines.append(DownLine)
    print(Upline, DownLine, MidLine)
    print(a.iloc[i]['Up'], a.iloc[i]['Down'], a.iloc[i]['Mid'])
    input()
