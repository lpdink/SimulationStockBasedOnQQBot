import threading
from dao.DataBaseOperator import DataBaseOperator
import time

global_flush_time = -1


def getNowPrice():
    return 0
    pass


# 首先查询表stock_information的所有股票编码stock_id，对每个stock_id：
# 调用API，查询当前价格now_price，利用time，得到刷新时间,历史价格置为-1，写入记录
# 刷新完毕后，调用函数flushAliveOrders()
# 结束后，设置定时器线程，global_flush_time*60秒后再次调用自身
def flushStockInformation():
    dbo = DataBaseOperator()
    dbo.openConnect()
    # 这个函数是我自己写的，会返回所有stock_id的list，非常Nice，果然dao就应该干一些脏活累活
    stock_id_list = dbo.searchAllRecordValue('stock_information', 'stock_id')
    for stock_id in stock_id_list:
        # TODO 改成写好的API函数
        now_price = getNowPrice()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        history_price = -1


if __name__ == "__main__":
    print(type(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
