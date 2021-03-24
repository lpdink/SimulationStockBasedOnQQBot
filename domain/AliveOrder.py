from sqlalchemy import Column, Text, Boolean, Float, DateTime, DECIMAL, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

BASE = declarative_base()


class AliveOrder(BASE):
    __tablename__ = 'alive_orders'
    user_id = Column(Text, primary_key=True)
    alive_order_index = Column(DECIMAL, primary_key=True)
    alive_order_time = Column(DateTime)
    buy_or_sell = Column(Boolean)
    stock_id = Column(Text)
    stock_name = Column(Text)
    stock_price = Column(DECIMAL)
    stock_amount = Column(DECIMAL)
    order_money_amount = Column(Float)
    is_alive = Column(Boolean)

    def __init__(self, user_id, alive_order_index, alive_order_time,
                 buy_or_sell, stock_id, stock_name, stock_price, stock_amount, order_money_amount,is_alive=True):
        self.user_id = user_id
        self.alive_order_index = alive_order_index
        self.alive_order_time = alive_order_time
        self.buy_or_sell = buy_or_sell
        self.stock_id = stock_id
        self.stock_name = stock_name
        self.stock_price = stock_price
        self.stock_amount = stock_amount
        self.order_money_amount = order_money_amount
        self.is_alive=is_alive

    def __str__(self):
        if self.buy_or_sell:
            bos = "买入"
        else:
            bos = "卖出"
        return "订单编号：{}\n订单时间：{}\n{}股票：{}\n数量：{}\n单价:{}\n订单总价格：{}".format(self.alive_order_index,
                                                                          self.alive_order_time, bos, self.stock_name,
                                                                          self.stock_amount, self.stock_price,
                                                                          self.order_money_amount)


if __name__ == "__main__":
    # 连接MySQL数据库，地址：localhost:3306,账号：root,密码：123,数据库：test
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/simulationstock?charset=utf8',
                           encoding='utf-8')
    DBSession = sessionmaker(bind=engine)

    session = DBSession()
    aliveorder = AliveOrder(user_id='906618000', alive_order_index=1, alive_order_time=datetime.now(),
                            buy_or_sell=True, stock_id='114514', stock_name='海豚证券', stock_price=5.12, stock_amount=10,
                            order_money_amount=51.2)
    session.add(aliveorder)

    session.commit()
    session.close()
