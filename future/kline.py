from hashlib import md5
from typing import List
import time

import numpy as np
from future import db


def getTime(ymdhm):
    timeStruct = time.strptime(ymdhm, '%Y-%m-%d %H:%M')
    return time.mktime(timeStruct)


class PERIOD:
    minute = 60
    five = 60 * 5
    half = 60 * 30
    hour = 3600
    day = 3600 * 24


def kline(a: List, period: int):
    """
    计算一批数据的k线,生成k线四元组ochl:open,close,high,low
    """
    t = [getTime(i[0]) for i in a]
    parts = []
    now = []
    beg = -1
    for i in range(len(a)):
        if beg == -1 or t[i] - t[beg] > period:
            if now:
                parts.append(now)
            now = [a[i]]
            beg = i
        else:
            now.append(a[i])
    if now:
        parts.append(now)
    ochl = []
    xs = []
    high = []
    low = []
    mid = []
    for part in parts:
        prices = [i[2] for i in part]
        xs.append(part[0][0])
        ochl.append([prices[0], prices[-1], max(prices), min(prices)])
        avg = int(np.mean(prices))
        high.append(avg + 10)
        mid.append(avg - 1)
        low.append(avg - 10)
    return {
        'x': xs,
        'y': ochl,
        'high': high,
        'mid': mid,
        'low': low,
    }


def get_kline(symbol, period: int):
    a = db.get_kline(symbol)
    res = kline(a, period)
    return res


if __name__ == '__main__':
    print(get_kline('M0', 60))
