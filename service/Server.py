from dao.DataBaseOperator import DataBaseOperator
from domain.AliveOrder import AliveOrder
from domain.GlobalVars import GlobalVars
from domain.StockInformation import StockInformation
from domain.UserInformation import UserInformation
from domain.UserHoldings import UserHoldings
from datetime import datetime
from FlushThread.FlushStockInformation import flushOneNow
from FlushThread.FlushStockInformation import flushAliveOrders
from domain.AllStock import AllStock
import tushare as ts
import requests
import json
import datetime

from dao.DataBaseOperator import DataBaseOperator
from domain.NAllStock import NAllStock

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec  # 分割子图
from mplfinance.original_flavor import candlestick2_ochl

begin_money = 500000
last_BTC = 58313.255


class Server:
    def outTime(self):
        today = datetime.now().isoweekday()
        if today == 6 or today == 7:
            return True
        hour = int(datetime.now().strftime('%H'))
        mint = int(datetime.now().strftime('%M'))
        now = hour + mint / 60
        if 9.5 <= now <= 11.5 or 13 <= now <= 15:
            return False
        return True

    async def register(self, user_id: str, user_name: str) -> str:
        dbo = DataBaseOperator()
        if dbo.searchOne(UserInformation, UserInformation.user_id, user_id):
            return "您已注册\n" + user_id + "\n" + user_name
        else:
            user = UserInformation(user_id=user_id, user_name=user_name,
                                   free_money_amount=begin_money, total_money_amount=begin_money)
            dbo.add(user)
            return "注册成功\n" + user_id + "\n" + user_name

    async def addSelfStock(self, stock_name: str) -> str:
        try:
            dbo = DataBaseOperator()
            obj = dbo.searchOne(StockInformation, StockInformation.stock_name, stock_name)
        except:
            return ""
        if obj:
            return "自选股已经被添加过\n" + obj.stock_name
        else:
            stock = dbo.searchOne(AllStock, AllStock.stock_name, stock_name)
            if stock:
                new_obj = StockInformation(stock_id=stock.stock_id, stock_name=stock_name, now_price=-1,
                                           flush_time=datetime.now(),
                                           up_down_rate=0)
                dbo.add(new_obj)
                flushOneNow(stock.stock_id)
                return "自选股添加成功\n" + str(stock_name)
            else:
                return "自选股添加失败，API缺少该股信息"

    async def addSelfStockWithID(self, stock_id: str) -> str:
        dbo = DataBaseOperator()
        obj = dbo.searchOne(StockInformation, StockInformation.stock_id, stock_id)
        if obj:
            return "自选股已经被添加过\n" + obj.stock_name
        else:
            try:
                df = ts.get_realtime_quotes(stock_id)
                stock_name = df['name'][0].replace(' ', '')
                now_price = float(df['price'])
                flush_time = datetime.strptime(df['date'][0] + " " + df['time'][0], '%Y-%m-%d %H:%M:%S')
            except:
                return "API缺少该股信息"
            try:
                up_down_rate = 100 * (float(df['price'][0]) - float(df['pre_close'][0])) / float(
                    df['pre_close'][0])
            except:
                up_down_rate = 0
            new_obj = StockInformation(stock_id=stock_id, stock_name=stock_name, now_price=now_price,
                                       flush_time=flush_time,
                                       up_down_rate=up_down_rate)
            try:
                dbo.add(new_obj)
            except:
                pass
            # 下面，添加到all_stock中
            new_stock = AllStock(stock_id=stock_id, stock_name=stock_name)
            dbo.add(new_stock)
            flushOneNow(stock_id)
            return "自选股添加成功\n" + str(stock_name)

    async def buyStock(self, user_id: str, stock_name: str, stock_amount: int, stock_price: float) -> str:
        if self.outTime():
            return "不在交易时间内"
        dbo = DataBaseOperator()
        if not dbo.searchOne(StockInformation, StockInformation.stock_name, stock_name):
            return "订单失败，请先添加自选股"
        else:
            aoi = dbo.searchAll(AliveOrder)
            if aoi:
                alive_order_index = aoi[-1].alive_order_index + 1
            else:
                alive_order_index = 1
            obj = dbo.searchOne(StockInformation, StockInformation.stock_name, stock_name)
            stock_id = obj.stock_id
            order_money_amount = stock_amount * stock_price
            try:
                free_money_amount = dbo.searchOne(UserInformation, UserInformation.user_id, user_id).free_money_amount
            except:
                return "没有找到您的信息，请先注册"
            if free_money_amount < order_money_amount:
                return "购买订单创建失败，可支配金额不足"
            else:
                alive_order = AliveOrder(user_id=user_id, alive_order_index=alive_order_index,
                                         alive_order_time=datetime.now(),
                                         buy_or_sell=True, stock_id=stock_id,
                                         stock_name=stock_name, stock_price=stock_price,
                                         stock_amount=stock_amount,
                                         order_money_amount=order_money_amount)
                dbo.add(alive_order)
                flushAliveOrders()
                return "购买订单创建成功\n股票：{}\n股数：{}\n预定价格：{}\n总价格：{}\n".format(stock_name, str(stock_amount),
                                                                          str(stock_price),
                                                                          str(order_money_amount))

    # 卖出：参数alive_order是类AliveOrder的实例，在service_main中实例化;
    # 请先根据alive_order的stock_index和user_id字段，调用双字段查询方法，查询表user_holdings的stock_amount
    # 如果查询不到，返回"卖出订单创建失败，您没有购买该支股票"
    # 如果查询到，比较查询到的stock_amount和alive_order的stock_amount
    # 如果查询到的较小，返回"卖出订单创建失败，您没有足够的持仓，当前持仓为："+str(查询到玩家持仓的stock_amount)
    # 如果玩家持仓较大，调用add_record方法，将str(alive_order)插入表alive_order中，返回"卖出订单创建成功"+str(订单id)
    async def sellStock(self, user_id: str, stock_name: str, stock_amount: int, stock_price: float) -> str:
        if self.outTime():
            return "不在交易时间内"
        dbo = DataBaseOperator()
        stock_amount_obj = dbo.searchOneWithTwoFields(UserHoldings, UserHoldings.stock_name, stock_name,
                                                      UserHoldings.user_id, user_id)
        if not stock_amount_obj:
            return "卖出订单创建失败，没有查询到您的持仓记录"
        else:
            now = datetime.now().strftime('%Y-%m-%d')
            bought_time = stock_amount_obj.bought_time.strftime('%Y-%m-%d')
            if now == bought_time:
                return "卖出订单创建失败，您必须在购买成功后的T+1日才能卖出"
            if stock_amount > stock_amount_obj.stock_amount:
                return "卖出订单创建失败，您没有足够的持仓，当前持仓为：" + str(stock_amount_obj.stock_amount)
            else:
                aoi = dbo.searchAll(AliveOrder)
                if aoi:
                    alive_order_index = aoi[-1].alive_order_index + 1
                else:
                    alive_order_index = 1
                try:
                    stock_id = dbo.searchOne(StockInformation, StockInformation.stock_name, stock_name).stock_id
                except:
                    return "卖出订单创建失败，自选股被非法删除，请联系管理员"
                alive_order = AliveOrder(user_id=user_id, alive_order_index=alive_order_index,
                                         alive_order_time=datetime.now(),
                                         buy_or_sell=False, stock_id=stock_id,
                                         stock_name=stock_name, stock_price=stock_price,
                                         stock_amount=stock_amount,
                                         order_money_amount=stock_amount * stock_price)

                dbo.add(alive_order)
                flushAliveOrders()
                return "卖出订单创建成功\n股票：{}\n股数：{}\n预定价格：{}\n总价格：{}\n".format(stock_name, str(stock_amount),
                                                                          str(stock_price),
                                                                          str(stock_amount * stock_price))

    async def searchUserHoldings(self, user_id: str) -> str:
        dbo = DataBaseOperator()
        dbo.delete(UserHoldings, UserHoldings.stock_amount, 0)
        userHoldings = dbo.searchAllWithField(UserHoldings, UserHoldings.user_id, user_id)
        if not userHoldings:
            return "您当前没有持仓"
        else:
            rst = "您好，{},您当前的持仓情况是：\n".format(user_id)
            if type(userHoldings) == list:
                for item in userHoldings:
                    rst += str(item) + "\n"
                    rst += "-------------\n"
            else:
                rst += str(userHoldings)

            return rst

    async def searchAliveOrders(self, user_id: str) -> str:
        dbo = DataBaseOperator()
        flushAliveOrders()
        dbo.delete(AliveOrder, AliveOrder.is_alive, False)
        aliveorders = dbo.searchAllWithField(AliveOrder, AliveOrder.user_id, user_id)
        if not aliveorders:
            return "您当前没有有效订单"
        else:
            rst = "您好，{},您当前的订单情况是：\n".format(user_id)
            if type(aliveorders) == list:
                for item in aliveorders:
                    rst += str(item) + "\n"
                    rst += "-------------\n"
            else:
                rst += str(aliveorders)

            return rst

    async def searchUserInformation(self, user_id: str) -> str:
        dbo = DataBaseOperator()
        user = dbo.searchOne(UserInformation, UserInformation.user_id, user_id)
        if not user:
            return "查询失败，您尚未注册"
        holdings = dbo.searchAllWithField(UserHoldings, UserHoldings.user_id, user_id)
        user.total_money_amount = 0
        for holding in holdings:
            try:
                price_now = dbo.searchOne(StockInformation, StockInformation.stock_name, holding.stock_name).now_price
                user.total_money_amount += holding.stock_amount * price_now
            except:
                return "查询个人信息失败，自选股被非法删除，请联系管理员"
        user.total_money_amount += user.free_money_amount
        dbo.update()
        rst = "您好，{},您当前的账户信息如下：\n".format(user_id)
        if type(user) == list:
            for item in user:
                rst += str(item) + "\n"
                rst += "-------------\n"
        else:
            rst += str(user)
        return rst

    async def searchStock(self):
        dbo = DataBaseOperator()
        objs = dbo.searchAll(StockInformation)
        rst = "股票名 价格 涨跌幅 更新时间\n"
        for obj in objs:
            rst += str(obj) + "\n--------\n"
        return rst

    async def cancelOrder(self, user_id: str, alive_order_index: int) -> str:
        dbo = DataBaseOperator()
        obj = dbo.searchOneWithTwoFields(AliveOrder, AliveOrder.user_id, user_id, AliveOrder.alive_order_index,
                                         alive_order_index)
        if not obj:
            return "您要删除的订单不存在"
        else:
            dbo.deleteWithTwoFields(AliveOrder, AliveOrder.user_id, user_id, AliveOrder.alive_order_index,
                                    alive_order_index)
            return "订单{}删除成功".format(obj.alive_order_index)

    async def deleteSelfStock(self, stock_name: str) -> str:
        dbo = DataBaseOperator()
        orders = dbo.searchAllWithField(AliveOrder, AliveOrder.stock_name, stock_name)
        holdings = dbo.searchAllWithField(UserHoldings, UserHoldings.stock_name, stock_name)
        if orders or holdings:
            return "已有订单或持仓，不能删除"
        else:
            if dbo.searchOne(StockInformation, StockInformation.stock_name, stock_name):
                dbo.delete(StockInformation, StockInformation.stock_name, stock_name)
                return stock_name + "删除成功"
            else:
                return "您要删除的自选股不存在，喂！不要乱玩这个功能！"

    async def help(self):
        s = "使用命令:\n！注册\n！添加 股票名\n！用编号添加 股票编号\n！删除 股票名\n" \
            + "！买入 股票名 购买价格 购买数量\n" + \
            "！卖出 股票名 卖出价格 卖出数量\n！持仓\n！订单\n！信息\n！取消订单 订单id" \
            + "\n！查询 股票名\n！用编号查询 股票编号" + "\n感谢您的使用"
        return s

    async def dzyPa(self):
        return "dzy爬"

    async def searchOneStock(self, stock_name):
        dbo = DataBaseOperator()
        try:
            stock_id = dbo.searchOne(AllStock, AllStock.stock_name, stock_name).stock_id
        except:
            return "查询失败，API缺少该股信息"
        obj = dbo.searchOne(StockInformation, StockInformation.stock_name, stock_name)
        if obj:
            if flushOneNow(stock_id):
                obj = dbo.searchOne(StockInformation, StockInformation.stock_name, stock_name)
                return str(obj)
            else:
                return "API查询失败，请稍后再次尝试"
        else:
            return "查询失败，请先添加自选股"

    async def searchOneStockWithID(self, stock_id):
        dbo = DataBaseOperator()
        obj = dbo.searchOne(StockInformation, StockInformation.stock_id, stock_id)
        if obj:
            if flushOneNow(stock_id):
                obj = dbo.searchOne(StockInformation, StockInformation.stock_id, stock_id)
                return str(obj)
            else:
                return "API查询失败，请稍后再次尝试"
        else:
            return "查询失败，请先添加自选股"

    async def getBTC(self):
        try:
            r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
            global last_BTC
            now_price = float(r.json()['bpi']['USD']['rate_float'])
            res = "BTC-USD：{:.3f}\n距上次查询幅度：{:.3f}%".format(now_price, 100 * (now_price - last_BTC) / last_BTC)
            if 100 * abs(last_BTC - now_price) / last_BTC > 3:
                last_BTC = now_price
                return "与上一次查询变化超过3%！\n" + res
            else:
                last_BTC = now_price
                return res
        except:
            return "ERROR: 请稍后尝试"

    async def getCryPto(self):
        try:
            try:
                r = requests.get('https://api.binancezh.co/api/v3/ticker/price', timeout=3)
            except:
                return "对API请求超时，你不够帅气"
            data = r.json()
            doge, ETH, BNB, BETHETH, BTCUSDT = 0, 0, 0, 0, 0
            for item in data:
                if item["symbol"] == "DOGEUSDT":
                    doge = float(item["price"])
                if item["symbol"] == "ETHUSDT":
                    ETH = float(item["price"])
                if item["symbol"] == "BNBUSDT":
                    BNB = float(item["price"])
                if item["symbol"] == "BETHETH":
                    BETHETH = float(item['price'])
                if item["symbol"] == "BTCUSDT":
                    BTCUSDT = float(item["price"])
            d = doge
            di = 0.0802888
            e = ETH
            ei = 1937.6
            pft = (((d - di) / di + (e - ei) / ei) / 2) * 100
            res = "DOGE：{:.6g}\nETH：{:.6g}\nBNB：{:.6g}\nBETH：{:.4g}\nBTC：{:.6g}\npft：{:.1f}%".format(doge, ETH, BNB,
                                                                                                     BETHETH,
                                                                                                     BTCUSDT, pft)
            return res
        except:
            return "ERROR: 请稍后尝试"

    async def rank(self):
        try:
            dbo = DataBaseOperator()
            users = dbo.searchAll(UserInformation)
            for i in range(len(users)):
                user = users[i]
                holdings = dbo.searchAllWithField(UserHoldings, UserHoldings.user_id, user.user_id)
                user.total_money_amount = 0
                for holding in holdings:
                    try:
                        price_now = dbo.searchOne(StockInformation, StockInformation.stock_name,
                                                  holding.stock_name).now_price
                        user.total_money_amount += holding.stock_amount * price_now
                    except:
                        return "查询个人信息失败，自选股被非法删除，请联系管理员"
                user.total_money_amount += user.free_money_amount
                dbo.update()
            users.sort(reverse=True, key=(lambda user: user.total_money_amount))
            rst = ""
            for i in range(0, len(users)):
                rst += "{}. {} {}\n".format(i + 1, users[i].user_name, users[i].total_money_amount)
            return rst
        except:
            return "连接数据库失败，请稍后重试"

    async def drawK(self, stock_name: str, deltatime: str):
        print(" i am here")
        deltatime = int(deltatime)
        dbo = DataBaseOperator()
        now = datetime.datetime.now().strftime('%Y%m%d')
        last = (datetime.datetime.now() - datetime.timedelta(days=deltatime)).strftime('%Y%m%d')
        print(now, last)
        pro = ts.pro_api('d2144df3d2c4f703454e331d9c95c0dc8685101ca04795d337cd5de1')
        try:
            code = dbo.searchOne(NAllStock, NAllStock.stock_name, stock_name).stock_id
        except:
            return "找不到该股票"
        try:
            df = pro.daily(ts_code=code, start_date=last, end_date=now)
        except:
            return "API错误：请稍后尝试"
        df_stockload = df[["trade_date", "open", "high", "low", "close", "vol"]]
        df_stockload = df_stockload.iloc[::-1]

        df_stockload['trade_date'] = pd.to_datetime(df_stockload['trade_date'])
        df_stockload = df_stockload.set_index('trade_date')

        np.seterr(divide='ignore', invalid='ignore')  # 忽略warning
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        fig = plt.figure(figsize=(20, 12), dpi=100, facecolor="white")  # 创建fig对象

        gs = gridspec.GridSpec(2, 1, left=0.08, bottom=0.15, right=0.99, top=0.96, wspace=None, hspace=0,
                               height_ratios=[3.5, 1])
        graph_KAV = fig.add_subplot(gs[0, :])
        graph_VOL = fig.add_subplot(gs[1, :])

        # 绘制K线图
        candlestick2_ochl(graph_KAV, df_stockload.open, df_stockload.close, df_stockload.high, df_stockload.low,
                          width=0.5,
                          colorup='r', colordown='g')  # 绘制K线走势

        # 绘制移动平均线图
        df_stockload['Ma5'] = df_stockload.close.rolling(
            window=5).mean()  # pd.rolling_mean(df_stockload.close,window=20)
        df_stockload['Ma10'] = df_stockload.close.rolling(
            window=10).mean()  # pd.rolling_mean(df_stockload.close,window=30)
        df_stockload['Ma20'] = df_stockload.close.rolling(
            window=20).mean()  # pd.rolling_mean(df_stockload.close,window=60)
        df_stockload['Ma30'] = df_stockload.close.rolling(
            window=30).mean()  # pd.rolling_mean(df_stockload.close,window=60)
        df_stockload['Ma60'] = df_stockload.close.rolling(
            window=60).mean()  # pd.rolling_mean(df_stockload.close,window=60)

        graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma5'], 'black', label='M5', lw=1.0)
        graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma10'], 'green', label='M10', lw=1.0)
        graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma20'], 'blue', label='M20', lw=1.0)
        graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma30'], 'pink', label='M30', lw=1.0)
        graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma60'], 'yellow', label='M60', lw=1.0)

        # 添加网格
        graph_KAV.grid()

        graph_KAV.legend(loc='best')
        graph_KAV.set_title("K")
        graph_KAV.set_ylabel(u"价格")
        graph_KAV.set_xlim(0, len(df_stockload.index))  # 设置一下x轴的范围

        # 绘制成交量图
        graph_VOL.bar(np.arange(0, len(df_stockload.index)), df_stockload.vol,
                      color=['g' if df_stockload.open[x] > df_stockload.close[x] else 'r' for x in
                             range(0, len(df_stockload.index))])
        graph_VOL.set_ylabel(u"成交量")
        graph_VOL.set_xlim(0, len(df_stockload.index))  # 设置一下x轴的范围
        graph_VOL.set_xticks(range(0, len(df_stockload.index), 15))  # X轴刻度设定 每15天标一个日期

        for label in graph_KAV.xaxis.get_ticklabels():
            label.set_visible(False)

        for label in graph_VOL.xaxis.get_ticklabels():
            label.set_visible(False)

        plt.savefig('/home/lpdink/home/lpdink/test/resource/data/images/Kline.png')
        print("save fig done...")
        return True


if __name__ == "__main__":
    server = Server()
    # print(server.register('906618000', 'xiaozeyu'))
    # print(server.buyStock('906618000', '114512', 500, 25))
    # print(server.sellStock('906618000', '海豚证券', 50, 10.5))
    # print(server.searchUserHoldings('906618000'))
    # print(server.searchAliveOrders('326490366'))
    # print(server.searchUserInformation('326490366'))
    # print(server.cancelOrder('22', 1))
    # print(server.addSelfStock('000553'))
    # print(server.buyStock('326490366','中国平安',1000,79.45))
    # print(server.searchUserInformation('326490366'))
    # print(server.addSelfStock('平安银行'))
    # print(server.addSelfStock("远望谷"))
    print(server.drawK("平安银行","365"))
