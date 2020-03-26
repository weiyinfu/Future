"""
利用新浪API获取期货小类
"""
import json
from os.path import *

import requests
from tqdm import tqdm

from sina import js

# 大类的路径
bigPath = join(dirname(__file__), './07-futureBig2.json')
productPath = join(dirname(__file__), 'products.json')
products = None
futures = None


def get(node):
    pageSize = 150
    url = f'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQFuturesData?page=1&num={pageSize}&node={node}&base=futures'
    content = requests.get(url).text
    return js.js_eval_json(content)


def load():
    global products, futures
    products = json.load(open(productPath))
    futures = []
    for market in products:
        for big in market['sons']:
            futures.extend(big['sons'])


def update_future():
    markets = json.load(open(bigPath))
    for market in markets:
        for big in tqdm(market['sons'], desc=f'正在爬取各个小类{market["name"]}'):
            sons = get(big['code'])
            products = []
            for son in sons:
                if son['exchange'] != market['code']:
                    print(son, market)
                    print(son['exchange'], market['code'])
                    exit(1)
                products.append({
                    "code": son['symbol'],
                    'name': son['name'],
                })
            big['sons'] = products
    json.dump(markets, open(productPath, 'w'), ensure_ascii=0, indent=2)


load()
if __name__ == '__main__':
    update_future()
