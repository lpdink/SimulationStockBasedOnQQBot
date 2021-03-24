import threading
from dao.DataBaseOperator import DataBaseOperator
from domain.StockInformation import StockInformation
from time import time
from datetime import datetime
import tushare as ts
from FlushThread.FlushAliveOrders import flushAliveOrders

global_flush_time = 3


# 首先查询表stock_information的所有股票编码stock_id，对每个stock_id：
# 调用API，查询当前价格now_price，利用time，得到刷新时间，写入记录
# 刷新完毕后，调用函数flushAliveOrders()
# 结束后，设置定时器线程，global_flush_time*60秒后再次调用自身
def flushStockInformation():
    dbo = DataBaseOperator()
    dbo.delete(StockInformation, StockInformation.stock_name, "API缺少该股信息")
    stock_list = dbo.searchAll(StockInformation)
    for stock in stock_list:
        try:
            df = ts.get_realtime_quotes(stock.stock_id)
            stock.stock_name = df['name'][0]
            stock.now_price = float(df['price'])
            stock.flush_time = datetime.strptime(df['date'][0] + " " + df['time'][0], '%Y-%m-%d %H:%M:%S')
            try:
                stock.up_down_rate = 100 * (float(df['price'][0]) - float(df['pre_close'][0])) / float(
                    df['pre_close'][0])
            except:
                stock.up_down_rate = 0
        except:
            stock.stock_name = "API缺少该股信息"
            stock.now_price = 9999
            stock.flush_time = datetime.now()
            stock.up_down_rate = 0
        dbo.update()
    flushAliveOrders()
    global timer
    timer = threading.Timer(global_flush_time * 60, flushStockInformation)


def flushOneNow(stock_id):
    dbo = DataBaseOperator()
    dbo.delete(StockInformation, StockInformation.stock_name, "API缺少该股信息")
    stock = dbo.searchOne(StockInformation, StockInformation.stock_id, stock_id)
    try:
        df = ts.get_realtime_quotes(stock.stock_id)
        stock.stock_name = df['name'][0]
        stock.now_price = float(df['price'])
        stock.flush_time = datetime.strptime(df['date'][0] + " " + df['time'][0], '%Y-%m-%d %H:%M:%S')
        try:
            stock.up_down_rate = 100 * (float(df['price'][0]) - float(df['pre_close'][0])) / float(
                df['pre_close'][0])
        except:
            stock.up_down_rate = 0
    except:
        stock.stock_name = "API缺少该股信息"
        stock.now_price = 9999
        stock.flush_time = datetime.now()
        stock.up_down_rate = 0
    dbo.update()
    return stock.stock_name


if __name__ == "__main__":
    flushStockInformation()
