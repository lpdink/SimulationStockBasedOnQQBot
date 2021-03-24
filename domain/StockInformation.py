from sqlalchemy import Column, Text, create_engine, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

BASE = declarative_base()


class StockInformation(BASE):
    __tablename__ = 'stock_information'
    stock_id = Column(Text, primary_key=True)
    stock_name = Column(Text)
    now_price = Column(Float)
    up_down_rate = Column(Float)
    flush_time = Column(DateTime)

    def __init__(self, stock_id, stock_name, now_price, up_down_rate, flush_time):
        self.stock_id = stock_id
        self.stock_name = stock_name
        self.now_price = now_price
        self.up_down_rate = up_down_rate
        self.flush_time = flush_time

    def __str__(self):
        return "{} {} {}% {}".format(self.stock_name, self.now_price,
                                     self.up_down_rate,
                                     self.flush_time)


if __name__ == "__main__":
    # 连接MySQL数据库，地址：localhost:3306,账号：root,密码：123,数据库：test
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/simulationstock?charset=utf8',
                           encoding='utf-8')
    DBSession = sessionmaker(bind=engine)

    session = DBSession()
    stockinformation = StockInformation(stock_id='114514', stock_name='海豚证券', now_price=5.28,
                                        flush_time=datetime.now(), up_down_rate=0)
    # session.add(stockinformation)
    print(stockinformation)

    # session.commit()
    session.close()
