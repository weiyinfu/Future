import logging
import threading
from os.path import *

from flask import Flask, jsonify, send_from_directory, request

import sina.api as sina
from future import fetcher
from future.myboll import myboll
from sina import futures
from future import kline

app = Flask(__name__)
cur = dirname(abspath(__file__))
dist_dir = join(cur, "../front/dist")


@app.route("/api/update")
def update():
    # 更新期货目录
    futures.update_future()
    return '更新期货目录成功'


@app.route("/api/get_data")
def get_data():
    # mock的数据
    return jsonify(myboll)


@app.route("/api/get_products")
def get_products():
    # 获取产品列表
    return jsonify(futures.products)


@app.route("/api/get_current")
def get_current():
    # 获取最新价格
    symbols = request.args['symbols'].split(',')
    return jsonify(sina.get_current(symbols))


@app.route("/api/get_kline")
def get_kline():
    # 获取k线
    symbol = request.args['symbol']
    period = int(request.args['period'])
    res = kline.get_kline(symbol=symbol, period=period)
    return jsonify(res)


@app.route("/<path:filename>")
def custom_static(filename):
    # 自定义static路径
    return send_from_directory(dist_dir, filename)


@app.before_first_request
def worker():
    logging.info('fetcher')
    # 此进程应为守护进程
    th = threading.Thread(
        target=fetcher.mainloop,
        daemon=True
    )
    th.start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7778, debug=True)
