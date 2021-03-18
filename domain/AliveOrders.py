class AliveOrder:
    def __init__(self, **kwargs):
        self.user_id = kwargs['user_id']
        self.alive_order_index = kwargs['alive_order_index']
        self.alive_order_time = kwargs['alive_order_time']
        self.buying_stock_index = kwargs['buying_stock_index']
        self.buying_stock_name = kwargs['buying_stock_name']
        self.buying_stock_amount = kwargs['buying_stock_amount']
        self.buying_stock_price = kwargs['buying_stock_price']
        self.order_money_amount = kwargs['order_money_amount']


if __name__ == "__main__":
    alive_order = AliveOrder(user_id=114514, alive_order_index=110260,
                                        alive_order_time=5, buying_stock_index=114514, buying_stock_name=500,
                                        buying_stock_amount=5, buying_stock_price=50, order_money_amount=500)
