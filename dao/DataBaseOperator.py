import pymysql
import configparser
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from domain.UserInformation import UserInformation

config = configparser.ConfigParser()
# 注意修改绝对路径，不要使用相对路径，否则在import时会keyError
config_file = 'E:/learn/2103/SimulationStockBasedOnQQBot/dao/dataBaseConfig.ini'
config.read(config_file, encoding='utf-8')
user = config['connect_mysql']['user']
password = config['connect_mysql']['password']
db = config['connect_mysql']['db']
host = config['connect_mysql']['host']
port = config['connect_mysql']['port']


class DataBaseOperator:
    # 构造函数
    def __init__(self):
        link = 'mysql+pymysql://' + user + ':' + password + '@' + host + ':' + port + '/' + db + '?charset=utf8'
        self.engine = create_engine(
            link,
            encoding='utf-8')

        self.DBSession = sessionmaker(bind=self.engine)

        self.session = self.DBSession()

    # 析构函数
    def __del__(self):
        self.session.close()

    # 增：obj：要增加的对象
    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    # 删:  CLASS：要删除对象的类 head: 表头, value: 值
    def delete(self, CLASS, head, value):
        self.session.query(CLASS).filter(head == value).delete()
        self.session.commit()

    def deleteWithTwoFields(self, CLASS, head1, value1, head2, value2):
        self.session.query(CLASS).filter(head1 == value1, head2 == value2).delete()
        self.session.commit()

    # 改:
    def update(self):
        self.session.commit()

    # 查：
    def searchAll(self, CLASS):
        return self.session.query(CLASS).all()

    def searchAllWithField(self, CLASS, head, value):
        return self.session.query(CLASS).filter(head == value).all()

    def searchOne(self, CLASS, head, value):
        return self.session.query(CLASS).filter(head == value).first()

    def searchOneWithTwoFields(self, CLASS, head1, value1, head2, value2):
        return self.session.query(CLASS).filter(head1 == value1, head2 == value2).first()


if __name__ == "__main__":
    dbo = DataBaseOperator()

    # 增测试
    # user = UserInformation(user_id='326490366', user_name='小布丁',
    #                       free_money_amount=50, total_money_amount=250)
    # dbo.add(user)

    # 删测试
    # dbo.delete(UserInformation, UserInformation.user_id, "326490366")

    # 查测试
    print(type(dbo.searchOneWithTwoFields(UserInformation,UserInformation.user_id,'326490366',UserInformation.user_name,'肖泽宇')))
