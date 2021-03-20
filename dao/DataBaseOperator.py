import pymysql
import configparser

config = configparser.ConfigParser()
# 注意修改绝对路径，不要使用相对路径，否则在import时会keyError
config_file = 'E:/learn/2103/SimulationStockBasedOnQQBot/dao/dataBaseConfig.ini'
config.read(config_file, encoding='utf-8')
user = config['connect_mysql']['user']
password = config['connect_mysql']['password']
db = config['connect_mysql']['db']
host = config['connect_mysql']['host']


class DataBaseOperator:
    def __init__(self):
        # connect是私有的，只能通过get方法访问.
        self.__connect = ""
        # 游标，通过游标进行数据库操作.
        self.__cursor = ""

    # 游标和连接一起创建
    def openConnect(self):
        self.__connect = pymysql.connect(user=user, passwd=password, db=db, host=host)
        self.__cursor = self.__connect.cursor()

    def getConnect(self):
        if self.__connect == "":
            raise Exception('[Error]: connect to mysql has not been opened or has been closed')
        else:
            return self.__connect

    def getCursor(self):
        if self.__cursor == "":
            raise Exception('[Error]: connect to mysql has not been opened or has been closed')
        else:
            return self.__cursor

    # 游标和连接一起关闭
    def closeConnect(self):
        if self.__cursor == "" or self.__connect == "":
            raise Exception('[Error]: connect to mysql has not been opened or has been closed')
        else:
            self.__cursor.close()
            self.__connect.close()
            self.__cursor, self.__connect = "", ""
            print("[Warning]: Connect to mysql has been closed.")

    # TODO
    # 实现功能后，请在下方__name__部分进行测试，确保与mysql数据库交互正常
    # 增：向表table(str)中插入记录record(str)
    # 成功后打印信息
    def addRecord(self, table, record):
        pass

    # 删：从表table(str)中删除主键(id)为primary_key(str)的记录
    # 成功后打印信息
    def deleteRecord(self, table, primary_key):
        pass

    # 删：删除表table(str)中两个字段组成一个主键的记录
    # 其中字段A为primary_key_A,字段B为primary_key_B
    # 成功后打印信息
    def deleteRecordWithTwoFields(self, table, primary_key_A, primaary_key_B):
        pass

    # 改：将表table(str)中主键（id)为primary_key(str)的记录，修改为record
    # 成功后打印信息
    def changeRecord(self, table, primary_key, record):
        pass

    # 查：返回表table(str)中主键(id)为primary_key的记录
    # 成功后打印信息
    def searchRecord(self, table, primary_key):
        pass

    # 查：返回表table(str)中主键(id)为primary_key的记录的表头为record_head的值
    # 成功后打印信息
    def searchRecordValue(self, table, primary_key, record_head):
        pass


    # 查：返回表table(str)中两个字段组成一个主键的记录
    # 其中字段A为primary_key_A,字段B为primary_key_B
    def searchRecordWithTwoFields(self, table, primary_key_A, primary_key_B):
        pass

    # 查：返回表table(str)中两个字段组成一个主键的记录的表头为record_head的值
    # 其中字段A为primary_key_A,字段B为primary_key_B
    def searchRecordWithTwoFieldsValue(self,table,primary_key_A,primary_key_B,record_head):
        pass

if __name__ == "__main__":
    operator = DataBaseOperator()
    operator.openConnect()
    print(operator.getConnect())
    print(operator.getCursor())
    operator.closeConnect()
