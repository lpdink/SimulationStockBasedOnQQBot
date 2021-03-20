class StockInformation:
    def __init__(self, **kwargs):
        self.stock_id = kwargs['stock_id']
        self.now_price = kwargs['now_price']
        self.flush_time = kwargs['flush_time']
        self.history_price = kwargs['history_price']

    def __str__(self):
        return "('{}',{},'{}',{})".format(self.stock_id, self.now_price,
                                          self.flush_time,
                                          self.history_price)


if __name__ == "__main__":
    stock_information = StockInformation(stock_id=110260, now_price=120,
                                         flush_time=5, history_price=500)
