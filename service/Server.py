from dao.DataBaseOperator import DataBaseOperator
from domain.AliveOrder import AliveOrder
from domain.GlobalVars import GlobalVars
from domain.StockInformation import StockInformation
from domain.UserInformation import UserInformation
from domain.UserHoldings import UserHoldings


class Server:
    # 注册：参数user_information是类UserInformation的实例，在service_main中实例化;
    # 请先检查user_information的user_id是否已经存在于表"user_information"中，如果存在，返回"您已注册\n"+str(user_id)
    # 否则，调用add_record方法，将str(user_information)，插入表user_information中，返回"注册成功"
    def register(self, user_information: UserInformation):
        dbo = DataBaseOperator()
        dbo.openConnect()
        if dbo.searchRecord("user_information", user_information.user_id):
            dbo.closeConnect()
            return "您已注册\n" + str(user_information.user_id)
        else:
            dbo.addRecord("user_information", str(user_information))
            dbo.closeConnect()
            return "注册成功" + str(user_information.user_id)

    # 添加自选股:参数stock_information是类StockInformation的实例，在service_main中实例化;
    # 请先检查stock_information的stock_id是否已经存在于表"stock_information"中，如果存在，返回"自选股已被添加过\n"+str(stock_id)
    # 否则，调用add_record方法，将str(stock_information)，插入表stock_information中，返回"自选股添加成功"
    def addSelfStock(self, stock_information: StockInformation):
        dbo = DataBaseOperator()
        dbo.openConnect()
        if dbo.searchRecord("stock_information", stock_information.stock_id):
            dbo.closeConnect()
            return "自选股已经被添加过\n" + str(stock_information.stock_id)
        else:
            dbo.addRecord("stock_information", str(stock_information))
            dbo.closeConnect()
            return "自选股添加成功" + str(stock_information.stock_id)

    # 买入：参数alive_order是类AliveOrder的实例，在service_main中实例化;
    # 请先根据alive_order的stock_index，查询表stock_information，如果不存在，返回"订单失败，请先添加自选股"
    # 如果存在，将alive_order的stock_name设置为返回结果中的stock_name项,将alive_order的stock_price设置为返回结果的stock_price项
    # 将order_money_amount项设置为stock_amount*stock_price
    # 根据alive_order的user_id，查询表user_information的free_money_amount项，比较free_money_amount和order_money_amount
    # 如果玩家钱不够，返回"购买订单创建失败：可支配金额不足"
    # 如果玩家钱够，调用add_record方法，将str(alive_order)插入表alive_order中，返回"购买订单创建成功"+str(订单id)
    def buyStock(self, alive_order: AliveOrder):
        dbo = DataBaseOperator()
        dbo.openConnect()
        if not dbo.searchRecord("stock_information", alive_order.stock_index):
            dbo.closeConnect()
            return "订单失败，请先添加自选股"
        else:
            alive_order.stock_name = dbo.searchRecordValue("stock_information", alive_order.stock_index, "stock_name")
            alive_order.stock_price = dbo.searchRecordValue("stock_information", alive_order.stock_index, "stock_price")
            alive_order.order_money_amount = alive_order.stock_amount * alive_order.stock_price
            free_money_amount = dbo.searchRecordValue("user_information", alive_order.user_id, "free_money_amount")
            # 这nm标识符命名还是有问题，都在alive_order下了，不是order的amount money，还能是nm的amount money吗？
            if free_money_amount < alive_order.order_money_amount:
                dbo.closeConnect()
                return "购买订单创建失败，可支配金额不足"
            else:
                dbo.addRecord("alive_orders", str(alive_order))
                dbo.closeConnect()
                return "购买订单创建成功" + str(alive_order.alive_order_index)

    # TODO
    # 请参考上面的实现，进行下面的实现
    # 卖出：参数alive_order是类AliveOrder的实例，在service_main中实例化;
    # 请先根据alive_order的stock_index和user_id字段，调用双字段查询方法，查询表user_holdings的stock_amount
    # 如果查询不到，返回"卖出订单创建失败，您没有购买该支股票"
    # 如果查询到，比较查询到的stock_amount和alive_order的stock_amount
    # 如果查询到的较小，返回"卖出订单创建失败，您没有足够的持仓，当前持仓为："+str(查询到玩家持仓的stock_amount)
    # 如果玩家持仓较大，调用add_record方法，将str(alive_order)插入表alive_order中，返回"卖出订单创建成功"+str(订单id)
    def sellStock(self, alive_order: AliveOrder):
        dbo = DataBaseOperator()
        dbo.openConnect()
        stock_amount = dbo.searchRecordWithTwoFieldsValue("user_holdings", alive_order.stock_index,
                                                          alive_order.user_id, "stock_amount")
        if not stock_amount:
            dbo.closeConnect()
            return "卖出订单创建失败，您没有足够的持仓，当前持仓为：" + str(alive_order.stock_amount)
        else:
            if stock_amount < alive_order.stock_amount:
                dbo.closeConnect()
                return "购买订单创建失败，可支配金额不足"
            else:
                dbo.addRecord("alive_orders", str(alive_order))
                dbo.closeConnect()
                return "卖出订单创建成功" + str(alive_order.alive_order_index)

    # 查询玩家持仓:
    # 根据user_id查询表user_holdings，如果不存在，返回"您当前没有持仓"
    # 如果存在，返回所有记录
    def searchUserHoldings(self, user_holdings: UserHoldings):
        dbo = DataBaseOperator()
        dbo.openConnect()
        userHoldings = dbo.searchRecord("user_holdings", user_holdings.user_id)
        if not userHoldings:
            dbo.closeConnect()
            return "您当前没有持仓"
        else:
            dbo.closeConnect()
            return userHoldings

    # 查询玩家订单:
    # 根据user_id查询表alive_orders，如果不存在，返回"您当前没有订单"
    # 如果存在，返回所有记录
    def searchAliveOrders(self, alive_order: AliveOrder):
        dbo = DataBaseOperator()
        dbo.openConnect()
        aliveOrders = dbo.searchRecord("alive_orders", alive_order.user_id)
        if not aliveOrders:
            dbo.closeConnect()
            return "您当前没有订单"
        else:
            dbo.closeConnect()
            return aliveOrders

    # 查询玩家信息:
    # 根据user_id查询表user_information,如果不存在，返回"系统出了bug，真奇怪，我们会把非玩家命令排除的...请联系管理员"
    # 如果存在，返回所有记录
    def searchUserInformation(self, user_information: UserInformation):
        dbo = DataBaseOperator()
        dbo.openConnect()
        userInformation = dbo.searchRecord("user_information", user_information.user_id)
        if not userInformation:
            dbo.closeConnect()
            return "系统出了bug，真奇怪，我们会把非玩家命令排除的...请联系管理员"
        else:
            dbo.closeConnect()
            return userInformation

    # 取消订单：
    # 根据user_id和alive_order_index查询表alive_orders,如果不存在，返回"您没有这条订单，请检查订单号"
    # 如果存在，调用delete方法，删除该记录,返回“取消订单成功”+str(订单id)
    def cancelOrder(self, alive_order: AliveOrder):
        dbo = DataBaseOperator()
        dbo.openConnect()
        if not dbo.searchRecordWithTwoFields("alive_orders", alive_order.user_id, alive_order.alive_order_index):
            dbo.closeConnect()
            return "您没有这条订单，请检查订单号"
        else:
            dbo.deleteRecordWithTwoFields("alive_orders", str(alive_order.user_id), str(alive_order.alive_order_index))
            dbo.closeConnect()
            return "取消订单成功" + str(alive_order.alive_order_index)


if __name__ == "__main__":
    dbo = DataBaseOperator()
    print("TODO.")
