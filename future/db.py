import sqlite3
import logging
from os.path import *
from typing import Dict, List
from tqdm import tqdm

db_file = join(dirname(__file__), '../future.db')
conn = sqlite3.connect(db_file, check_same_thread=False)


def exist_structure():
    """
    判断数据库结构是否存在
    """
    res = conn.execute("SELECT * FROM sqlite_master WHERE tbl_name='future'")
    return res.fetchone() is not None


def init_structure():
    """
    初始化数据库表结构
    """
    logging.info('正在初始化数据库')
    conn.executescript(
        """
DROP TABLE  IF EXISTS  future ;
DROP TABLE  IF EXISTS  tag ;
create table future (
    time datetime,
    symbol varchar(15),
    price float,
    hold int
);
create table tag(
    symbol varchar(15) primary key,
    tag varchar(128)
);
        """
    )
    conn.commit()


def insert(item: Dict):
    """
    向数据库中插入一个期货价格记录
    """
    sql = f"""
    insert into future(time,symbol,price,hold) values
    ('{item['time']}','{item['symbol']}', '{item['price']}', '{item['hold']}')
    """
    logging.debug(f"插入数据 {sql}")
    conn.execute(sql)
    conn.commit()


def insert_many(a: List[Dict]):
    sql = f"""
insert into future(time,symbol,price,hold)values(?,?,?,?)
"""
    logging.debug(f"插入多条数据{sql}")
    batch_size = 1000
    for i in tqdm(range(0, len(a), batch_size), desc='批量插入数据'):
        conn.executemany(sql, a[i:i + batch_size])
    conn.commit()


def get_tag(symbol: str):
    sql = f"""
select tag from tag where symbol = '{symbol}'
"""
    logging.debug(f"获取tag {sql}")
    res = conn.execute(sql)
    a = res.fetchall()
    if not a:
        return
    tag = a[0][0]
    return tag


def put_tag(symbol: str, tag: str):
    sql = f"""
replace into tag(symbol,tag) values('{symbol}','{tag}') 
"""
    conn.execute(sql)
    conn.commit()


def get_kline(symbol):
    cur = conn.execute(f"""
select * from future where symbol='{symbol}' order by time
""")
    res = cur.fetchall()
    return res


if not exist_structure():
    init_structure()

if __name__ == '__main__':
    from pprint import pprint

    a = get_kline('M0')
    print(a)
    for i in range(len(a[0])):
        print(type(a[0][i]))
