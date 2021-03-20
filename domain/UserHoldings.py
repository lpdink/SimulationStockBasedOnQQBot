class UserHoldings:
    def __init__(self, **kwargs):
        self.user_id = kwargs['user_id']
        self.stock_index = kwargs['stock_index']
        self.stock_amount = kwargs['stock_amount']
        self.bought_price = kwargs['bought_price']
        self.bought_total_price = kwargs['bought_total_price']

    def __str__(self):
        return "('{}','{}',{},{},{})".format(self.user_id, self.stock_index,
                                             self.stock_amount,
                                             self.bought_price,
                                             self.bought_total_price)


if __name__ == "__main__":
    user_holdings = UserHoldings(user_id=114514, stock_index=110260,
                                 stock_amount=5, bought_price=50, bought_total_price=500)
