from service.Server import Server
from dao.DataBaseOperator import DataBaseOperator
from domain.AliveOrder import AliveOrder
from domain.GlobalVars import GlobalVars
from domain.StockInformation import StockInformation
from domain.UserInformation import UserInformation
from domain.UserHoldings import UserHoldings


class Handler:
    async def register(self, user_id: str, user_name: str) -> str:
        user_information = UserInformation(user_id=user_id, user_name=user_name,
                                           free_money_amount=500000, total_money_amount=500000,
                                           history_money_amount=500000)
        server = Server()
        return server.register(user_information)

    async def addSelfStock(self, stock_id: str) -> str:
        stock_information = StockInformation(stock_id=stock_id, now_price=-1, flush_time='-1', history_price=-1)
        server = Server()
        return server.addSelfStock(stock_information)

    # TODO
    # 请参考register和addSelfStock的定义，完成以下6个方法的定义
    # 注意返回值都是str的
    # 在实例化实体类时，请传入合适的参数，如果参数不属于用户应该传入的，按照类型传入-1，"-1"等等
    async def buyStock(self, user_id: str, stock_index: str, stock_amount: int, stock_price: float) -> str:
        pass

    async def sellStock(self, user_id: str, stock_index: str, stock_amount: int, stock_price: float) -> str:
        pass

    async def searchUserHoldings(self, user_id: str) -> str:
        pass

    async def searchAliveOrders(self, user_id: str) -> str:
        pass

    async def searchUserInformation(self, user_id: str) -> str:
        pass

    async def cancelOrder(self, user_id: str, alive_order_index: str) -> str:
        pass
