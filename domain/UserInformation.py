from sqlalchemy import Column, Text, create_engine, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class UserInformation(BASE):
    __tablename__ = 'user_information'
    user_id = Column(Text, primary_key=True)
    user_name = Column(Text)
    free_money_amount = Column(Float)
    total_money_amount = Column(Float)

    def __init__(self, user_id, user_name, free_money_amount, total_money_amount):
        self.user_id = user_id
        self.user_name = user_name
        self.free_money_amount = free_money_amount
        self.total_money_amount = total_money_amount

    def __str__(self):
        return "昵称：{}\n可支配金额：{}\n总资产：{}".format(self.user_name, self.free_money_amount, self.total_money_amount)


if __name__ == "__main__":
    # 连接MySQL数据库，地址：localhost:3306,账号：root,密码：123,数据库：test
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/simulationstock?charset=utf8',
                           encoding='utf-8')
    DBSession = sessionmaker(bind=engine)

    session = DBSession()
    t = session.query(UserInformation).first()
    print(t)
    session.close()
