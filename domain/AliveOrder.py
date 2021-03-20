class AliveOrder:
    def __init__(self, **kwargs):
        self.user_id = kwargs['user_id']
        self.alive_order_index = kwargs['alive_order_index']
        self.alive_order_time = kwargs['alive_order_time']
        self.buy_or_sell = kwargs['buy_or_sell']
        self.stock_index = kwargs['stock_index']
        self.stock_name = kwargs['stock_name']
        self.stock_amount = kwargs['stock_amount']
        self.stock_price = kwargs['stock_price']
        self.order_money_amount = kwargs['order_money_amount']

    def __str__(self):
        return "('{}','{}','{}',{},'{}','{}',{},{},{})".format(self.user_id, self.alive_order_index,
                                                               self.alive_order_time,
                                                               self.buy_or_sell,
                                                               self.stock_index,
                                                               self.stock_name,
                                                               self.stock_amount,
                                                               self.stock_price,
                                                               self.order_money_amount)


if __name__ == "__main__":
    alive_order = AliveOrder(user_id=114514, alive_order_index=110260,
                             alive_order_time=5, buy_or_sell=1, stock_index=114514, stock_name=500,
                             stock_amount=5, stock_price=50, order_money_amount=500)
