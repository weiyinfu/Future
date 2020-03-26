import json

a = json.load(open('./data.json'))
from future import db

a = [(i['time'], i['symbol'], i['price'], i['hold']) for i in a]
db.insert_many(a)
