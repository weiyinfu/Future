"""
获取小类的行情
"""
import re
from pprint import pprint
from typing import List

import requests


class KLineType:
    """
    k线的类型
    """
    Minute5 = "MiniKLine5m"
    Minute15 = "MiniKLine15m"
    Minute30 = "MiniKLine30m"
    Minute60 = "MiniKLine60m"
    Day = "DailyKLine"



def get_kline(symbol, kline_type):
    url = f"http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFutures{kline_type}?symbol={symbol}"
    return requests.get(url).json()


def get_current(symbols: List[str]):
    url = f"http://hq.sinajs.cn/list={','.join(symbols)}"
    content = requests.get(url).text
    lines = content.splitlines()
    a = {}
    for line in lines:
        k, v = line.split('=')
        symbol = k.split()[1]
        if symbol.startswith('hq_str_'):
            symbol = symbol[len('hq_str_'):]
        values = v.strip(';').strip('"').split(',')
        values = [i for i in values if i]  # 去掉空元素
        if not values:
            continue
        for i in range(len(values)):
            if re.match(r'^\d+(\.\d+)?$', values[i]):
                values[i] = float(values[i])
        obj = {
            '开盘价': values[2],
            '最高价': values[3],
            '最低价': values[4],
            '买入': values[6],
            '卖出': values[7],
            '最新价': values[8],
            '昨日结算': values[10],
            '买量': values[11],
            '卖量': values[12],
            '持仓量': values[13],
            '成交量': values[14],
        }
        a[symbol] = obj
    return a


def test_kline():
    pprint(get_kline('M0', KLineType.Minute5))


def test_current():
    pprint(get_current(['M0', 'SC2106']))


if __name__ == '__main__':
    test_current()
