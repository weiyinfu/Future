import datetime
now=datetime.datetime.now()
print(now.strftime('%Y-%m-%d %H:%M:%S'))
print(now+datetime.timedelta(minutes=1))