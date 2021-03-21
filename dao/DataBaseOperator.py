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

    # 改:
    # 需要的参数太多，请需要改操作时，向TODO里添加需求，说明输入输出

    # 查：
    def searchAll(self, CLASS):
        return self.session.query(CLASS).all()


if __name__ == "__main__":
    dbo = DataBaseOperator()

    # 增测试
    # user = UserInformation(user_id='326490366', user_name='小布丁',
    #                       free_money_amount=50, total_money_amount=250)
    # dbo.add(user)

    # 删测试
    # dbo.delete(UserInformation, UserInformation.user_id, "326490366")

    # 查测试
    print(dbo.searchAll(UserInformation))
