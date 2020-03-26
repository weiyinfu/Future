"""
为了第一次运行,准备初始数据,爬取所有品类的5分钟k线数据
把kline数据转成4个时刻+数据的形式
"""

import datetime
import json

from tqdm import tqdm

from sina import api
from sina import futures

all_futures = futures.futures
data = []
for f in tqdm(all_futures, desc='正在爬取kline'):
    print(f)
    ans = api.get_kline(f['code'], api.KLineType.Minute5)
    for it in ans:
        t, op, high, low, close, hold = it
        t = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
        prices = [op, high, low, close]
        for i in range(len(prices)):
            now = (t + datetime.timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M')
            data.append({
                'time': now,
                'symbol': f['code'],
                'price': prices[i],
                'hold': hold,
            })
json.dump(data, open('data.json', 'w'), ensure_ascii=0, indent=2)
