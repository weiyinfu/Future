新浪财经：https://finance.sina.com.cn/futures/quotes/M0.shtml  

新浪财经API接口综述：
* 获取各大期货市场的一级代码
* 根据一级代码获取二级代码，二级代码就是具体的期货代号了
* 根据期货代号获取期货最新行情
* 根据期货代号获取K线，包括5分k线，10分k线，1天k线等。  

全部期货列表：
http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_0  
从此链接可以看出很多API接口。  

# 接口一：获取全部期货产品类别
http://vip.stock.finance.sina.com.cn/quotes_service/view/js/qihuohangqing.js

在这个期货行情.js中列出了各个期货市场的产品代码。根据产品大类可以获取具体的期货代码。产品大类基本上是不变化的。  

# 接口二：获取期货代码
有了期货大类，就可以求出期货小类。  
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQFuturesData?page=1&num=150&sort=position&asc=0&node=zly_qh&base=futures

这个请求中的node就是期货大类代码。


# 接口三：实时数据
此接口有多种类型的参数:一种直接写symbol,另一种带着nf前缀
http://hq.sinajs.cn/list=M0  
https://hq.sinajs.cn/?_=1585150001745/&list=nf_RB2005,nf_M0,nf_TF0  
M0表示期货代码。返回值为
```typescript
var hq_str_M0="豆粕连续,145958,3170（开盘价）,3190（最高价）,3145（最低价）,3178（昨日收盘价）,3153（买价）,3154（卖价）,3154（最新价）,3162（结算价）,3169（昨结算）,1325（买量）,223（卖量）,1371608（持仓量）,1611074（成交量）,连,豆粕,2013-06-28";
```
每个字段的含义，可以根据JavaScript推测得出：
http://vip.stock.finance.sina.com.cn/quotes_service/view/js/stock_list_futuresgoods.js
```js
const filed={f:'symbol', t:'代码', d:-2, s:48},
			{f:'name', t:'名称', d:-2, s:50},
			{f:'trade', t:'最新价', d:-1, s:64,c:'colorize'},
			{f:'change', t:'涨跌', d:-1, s:4, c:'colorize'},
			{f:'buyprice', t:'买价', d:-1, s:64,c:'colorize'},
			{f:'buyvol', t:'买量', d:-1, s:64, c:'colorize'},
			{f:'sellprice', t:'卖价', d:-1, s:64, c:'colorize'},
			{f:'sellvol', t:'卖量', d:-1,s:64, c:'colorize'},
			{f:'volume', t:'成交量', d:-1, s:64, c:'colorize'},
			{f:'todayopen', t:'今开盘', d:-1, s:64, c:'colorize'},
			{f:'yesterdaysettlement', t:'昨结算', d:-1, s:64, c:'colorize'},
			{f:'high', t:'最高价', d:-1, s:64, c:'colorize'},
			{f:'low', t:'最低价', d:-1, s:64, c:'colorize'}
```
每个字段的含义也可以比对UI`http://finance.sina.com.cn/futures/quotes/M0.shtml`看出：
```plain
最新价:  3154 
开盘价:  3170 
最高价:  3190   
最低价:  3145
结算价:  3162 
昨结算:  3169 
持仓量:  1371608 
成交量:  1611074
买  价:  3153 
卖  价:  3154 
买  量:  1325  
卖  量:  223
```

此接口一次可以请求多个品种：http://hq.sinajs.cn/list=CFF_RE_IF1307,TA0,M0

# 接口四：商品期货历史K线图
返回值为:开高低收

http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLineXm?symbol=CODE
例子： 
5分钟http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine5m?symbol=M0
15分钟
http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine15m?symbol=M0
30分钟
http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine30m?symbol=M0
60分钟
http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine60m?symbol=M0
日K线
http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=M0
http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=M1401

另一种接口是jsonp接口:
https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_RB2005_5_1585150008277=/InnerFuturesNewService.getFewMinLine?symbol=RB2005&type=5

# 接口五：股指期货
股指期货 5分钟
http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine5m?symbol=IF1306
 
15
http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine15m?symbol=IF1306
30分钟
http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine30m?symbol=IF1306

60分钟
http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine60m?symbol=IF1306

日线
http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesDailyKLine?symbol=IF1306