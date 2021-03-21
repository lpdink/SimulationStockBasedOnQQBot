from dao.DataBaseOperator import DataBaseOperator


# 查询alive_orders表，如果为空，返回。
# 如果不为空，查询alive_orders表的所有记录，记为order_records
# 对每条记录order_record，如果buy_or_sell为1（买入）：
#       按照stock_id，查询表stock_information的now_price字段
#       如果now_price较小，准备按照order_record的stock_price买入，否则continue到下一条order_record记录
#       查询order_record的order_money_amount字段
#       根据order_record的user_id，查询表user_information的free_money_amount字段
#       比较order_money_amount字段与free_money_amount字段
#           如果free_money_amount>=order_money_amount，买入成功：
#               修改user_information的free_money_amount为free_money_amount-order_money_amount
#               查询user_holdings是否有user_id+stock_index的记录，如果有，user_holdings的stock_amount+=order_record的
def flushAliveOrders():
    pass
