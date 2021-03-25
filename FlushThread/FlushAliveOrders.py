from dao.DataBaseOperator import DataBaseOperator
from domain.AliveOrder import AliveOrder
from domain.StockInformation import StockInformation
from domain.UserInformation import UserInformation
from domain.UserHoldings import UserHoldings
from datetime import datetime


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
# 卖出订单：
#   查询表UserInformation的now_price，如果价格低于order的价格，continue
#   否则，查询user_holdings的stock_amount字段，比较order的amount和holdings的amount，如果order的大，continue。
#   否则，user的free_money_amount字段+=order的money_amount字段-手续费。holdings-=amount，order的is_alive设为false
def flushAliveOrders():
    dbo = DataBaseOperator()
    dbo.delete(AliveOrder, AliveOrder.is_alive, False)
    dbo.delete(UserHoldings, UserHoldings.stock_amount, 0)
    order_list = dbo.searchAll(AliveOrder)
    for order in order_list:
        # True是买入
        if order.buy_or_sell:
            stock = dbo.searchOne(StockInformation, StockInformation.stock_id, order.stock_id)
            print(stock.now_price,order.stock_price,stock.stock_name)
            if stock.now_price <= order.stock_price:
                # 买入
                user = dbo.searchOne(UserInformation, UserInformation.user_id, order.user_id)
                service_charge = order.order_money_amount * 0.0003
                if service_charge < 5:
                    service_charge = 5
                order.order_money_amount = order.stock_amount * stock.now_price
                if order.order_money_amount <= user.free_money_amount + service_charge:
                    user.free_money_amount -= (order.order_money_amount + service_charge)
                    order.is_alive = False
                    holdings = dbo.searchOneWithTwoFields(UserHoldings, UserHoldings.user_id, order.user_id,
                                                          UserHoldings.stock_name, order.stock_name)
                    if holdings:
                        holdings.stock_amount += order.stock_amount
                        holdings.bought_price = order.stock_price
                        holdings.bought_total_price += order.order_money_amount
                    else:
                        holdings = UserHoldings(order.user_id, order.stock_name, order.stock_amount, stock.stock_price,
                                                order.order_money_amount, datetime.now())
                        dbo.add(holdings)
                dbo.update()
            else:
                continue
                # 卖出订单：
                #   查询表UserInformation的now_price，如果价格低于order的价格，continue
                #   否则，查询user_holdings的stock_amount字段，比较order的amount和holdings的amount，如果order的大，continue。
                #   否则，user的free_money_amount字段+=order的money_amount字段-手续费。holdings-=amount，order的is_alive设为false
        else:
            stock = dbo.searchOne(StockInformation, StockInformation.stock_id, order.stock_id)
            if stock.now_price > order.stock_price:
                holdings = dbo.searchOne(UserHoldings, UserHoldings.user_id, order.user_id)
                if holdings.stock_amount >= order.stock_amount:
                    service_charge = order.stock_amount * stock.now_price * 0.0013
                    if service_charge < 5:
                        service_charge = 5
                    user = dbo.searchOne(UserInformation, UserInformation.user_id, order.user_id)
                    user.free_money_amount += stock.now_price * order.stock_amount - service_charge
                    holdings.stock_amount -= order.stock_amount
                    order.is_alive = False
                else:
                    continue
            else:
                continue
            dbo.update()


if __name__ == "__main__":
    flushAliveOrders()
