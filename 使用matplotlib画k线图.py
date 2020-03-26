import mplfinance as f
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

print(a.head(3))
n = len(a)
# adds = [f.make_addplot(a[i][:n], scatter=False) for i in "Up Mid Low".split()]
adds = f.make_addplot(a[['Up', "Mid", "Down"]][:n], scatter=False)
f.plot(a[:n],
       type="candle",
       addplot=adds,
       volume=True,
       style='starsandstripes', figscale=1.2)
print(f.available_styles())