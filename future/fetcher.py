"""
定时爬取数据

每分钟爬取一次数据，由于不同期货有不同的交易时间,所以给每次请求的结果打上一个tag，如果此次tag与上次请求得到的tag相同，说明交易已经停止了，不再更新数据库。只有在获取到的数据与上次数据不同时才更新数据库.
"""
import schedule
import time
import sina.api as sina
from future import db
import datetime
import logging
from sina import futures
from future import util
from typing import List, Dict

last_datetime = 0


def get_tag(future_data: Dict):
    # 使用hashMap
    a = list(future_data.items())
    a = sorted(a, key=lambda x: x[0])
    s = ''.join(str(i) for i in a)
    return util.md5_str(s)


def crawl():
    global last_datetime
    # 当前时间
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    if last_datetime == now:
        # 上一次的时间戳与此次时间戳相同，直接返回
        logging.debug('时间戳相同')
        return
    last_datetime = now
    # 请求所有的期货
    symbols = [i['code'] for i in futures.futures]
    res: Dict = sina.get_current(symbols)
    for symbol, v in res.items():
        cur_tag = get_tag(v)
        last_tag = db.get_tag(symbol)
        if cur_tag == last_tag:
            # 如果两次tag相同，不插入到数据库
            logging.debug('tag相同跳过')
            continue
        db.insert({
            'time': now,
            'symbol': symbol,
            'price': v['最新价'],
            'hold': v['持仓量'],
        })
        db.put_tag(symbol, cur_tag)


def mainloop():
    logging.debug('fetcher mainloop')
    job = schedule.every(0.9).minutes.do(crawl)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    mainloop()
