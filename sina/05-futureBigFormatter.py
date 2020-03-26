"""
把furtureBig这个文件格式化一下

原油期货属于上海国际能源交易中心
"""
import json

a = json.load(open('03-futureBig.json'))
markets = []

errors = ['yy_qh', 'ehj_qh']


def parseMarket(market):
    return {
        'name': market[0],
        'futures': [{'name': i[0], 'code': i[1]} for i in market[1:] if i[1] not in errors]
    }


for i in a:
    market = parseMarket(a[i])
    markets.append({
        'code': i,
        'name': market['name'],
        'sons': market['futures'],
    })
markets.append({
    'code': 'ine',
    'name': '上海国际能源交易中心',
    'sons': [{
        'name': '原油',
        'code': 'yy_qh'
    }, {
        'name': '20号胶连续',
        'code': 'ehj_qh'
    }
    ]
})
print(markets)
json.dump(markets, open('07-futureBig2.json', 'w'), ensure_ascii=0, indent=2)

"""
测试一下不同的期货市场是否有不同的产品
"""
all_futures = []
for market in markets:
    all_futures.extend(market['sons'])
print(len(all_futures))
from collections import Counter

"""
结果表明，不同的期货市场所具有的期货大类是完全不同的
"""
print(Counter([i['code'] for i in all_futures]))

"""
打印一下
"""
for market in markets:
    print(market['name'])
    print(','.join(i['name'] for i in market['sons']))
