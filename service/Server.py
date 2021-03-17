import sys

sys.path.append("../dao/")
import DataBaseOperator

sys.path.append("../domain/")
import AliveOrders
import GlobalVars
import StockInformation
import UserHoldings
import UserInformation


class Server:
    def register(self):
        pass

    def addSelfStock(self):
        pass

    def buyStock(self):
        pass

    def sellStock(self):
        pass

    # 根据需要，这里需要多种search
    def searchInformation(self):
        pass

    def cancelOrder(self):
        pass

if __name__=="__main__":
    print("TODO.")
