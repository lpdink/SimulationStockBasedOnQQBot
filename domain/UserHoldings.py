from sqlalchemy import Column, Text, DECIMAL, create_engine, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class UserHoldings(BASE):
    __tablename__ = 'user_holdings'
    user_id = Column(Text, primary_key=True)
    stock_name = Column(Text, primary_key=True)
    stock_amount = Column(DECIMAL)
    bought_price = Column(DECIMAL)
    bought_total_price = Column(DECIMAL)
    bought_time = Column(DateTime)

    def __init__(self, user_id, stock_name, stock_amount, bought_price, bought_total_price, bought_time):
        self.user_id = user_id
        self.stock_name = stock_name
        self.stock_amount = stock_amount
        self.bought_price = bought_price
        self.bought_total_price = bought_total_price
        self.bought_time = bought_time

    def __str__(self):
        return "股票名:{}\n持有股数:{}\n购买时价格:{}\n购买时间:{}".format(self.stock_name, self.stock_amount,
                                                           self.bought_price, self.bought_time)


if __name__ == "__main__":
    # 连接MySQL数据库，地址：localhost:3306,账号：root,密码：123,数据库：test
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/simulationstock?charset=utf8',
                           encoding='utf-8')
    DBSession = sessionmaker(bind=engine)

    session = DBSession()
    userholdings = UserHoldings(user_id='326490366', stock_name='壁画银行', stock_amount=50, bought_price=2.5,
                                bought_total_price=125.0)
    print(userholdings)
    session.add(userholdings)

    session.commit()
    session.close()
