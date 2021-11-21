from dao.DataBaseOperator import DataBaseOperator
from domain.AliveOrder import AliveOrder
from domain.GlobalVars import GlobalVars
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


def showExpection(a_func):
    async def wrapTheFunction(*args, **kwargs):
        try:
            return a_func(*args, **kwargs)
        except Exception as E:
            print("!!!!!!\n", E, "\n!!!!!!")
            return str(E)

    return wrapTheFunction


class Server:
    def outTime(self):
        today = datetime.datetime.now().isoweekday()
        if today == 6 or today == 7:
            return True
        hour = int(datetime.datetime.now().strftime('%H'))
        mint = int(datetime.datetime.now().strftime('%M'))
        now = hour + mint / 60
        if 9.5 <= now <= 11.5 or 13 <= now <= 15:
            return False
        return True

    def getPrice(self, stock_id: str):
        df = ts.get_realtime_quotes(stock_id)
        return float(df['price'][0])

    @showExpection
    def register(self, user_id: str, user_name: str) -> str:
        dbo = DataBaseOperator()
        if dbo.searchOne(UserInformation, UserInformation.user_id, user_id):
            return "您已注册\n" + user_id + "\n" + user_name
        else:
            user = UserInformation(user_id=user_id, user_name=user_name,
                                   free_money_amount=begin_money, total_money_amount=begin_money)
            dbo.add(user)
            return "注册成功\n" + user_id + "\n" + user_name

    @showExpection
    def buyStock(self, user_id: str, stock_name: str, stock_amount: int) -> str:
        #if self.outTime():
        #    return "购买失败：请等到开盘"
        dbo = DataBaseOperator()
        obj = dbo.searchOne(AllStock, AllStock.stock_name, stock_name)
        if not obj:
            return "购买失败：没有找到该支股票"
        else:
            stock_id = obj.stock_id
            stock_price = self.getPrice(stock_id)
            order_money_amount = stock_amount * stock_price
            try:
                user = dbo.searchOne(UserInformation, UserInformation.user_id, user_id)
                free_money_amount = user.free_money_amount
            except:
                return "没有找到您的信息，请先注册"
            # 买入
            service_charge = order_money_amount * 0.0003
            service_charge = max(service_charge, 5)
            total_cost = int(order_money_amount + service_charge)
            if free_money_amount < total_cost:
                return "购买失败：可支配金额不足"
            else:
                user.free_money_amount -= total_cost
                holdings = dbo.searchOneWithTwoFields(UserHoldings, UserHoldings.user_id, user_id,
                                                      UserHoldings.stock_name, stock_name)
                if holdings:
                    holdings.stock_amount += stock_amount
                    holdings.bought_price = stock_price
                    holdings.bought_total_price += order_money_amount
                    holdings.bought_time = datetime.datetime.now()
                else:
                    holdings = UserHoldings(user_id, stock_name, stock_amount, stock_price,
                                            order_money_amount, datetime.datetime.now())
                    dbo.add(holdings)
            dbo.update()
            return "购买成功\n股票：{}\n股数：{}\n总价格：{}\n剩余可支配金额：{}".format(stock_name, str(stock_amount),
                                                                   str(total_cost),
                                                                   str(user.free_money_amount))

    @showExpection
    def sellStock(self, user_id: str, stock_name: str, stock_amount: int) -> str:
        #if self.outTime():
        #    return "卖出失败：请等待开盘"
        dbo = DataBaseOperator()
        holdings = dbo.searchOneWithTwoFields(UserHoldings, UserHoldings.stock_name, stock_name,
                                              UserHoldings.user_id, user_id)
        if not holdings:
            return "卖出失败:没有查询到您的持仓记录"
        else:
            now = datetime.datetime.now().strftime('%Y-%m-%d')
            bought_time = holdings.bought_time.strftime('%Y-%m-%d')
            if now == bought_time:
                return "卖出失败:您必须在购买成功后的T+1日才能卖出"
            if stock_amount > holdings.stock_amount:
                return "卖出失败:您没有足够的持仓，当前持仓为：" + str(holdings.stock_amount)
            else:
                stock = dbo.searchOne(AllStock, AllStock.stock_name, stock_name)
                now_price = self.getPrice(stock.stock_id)
                service_charge = stock_amount * now_price * 0.0013
                service_charge = max(service_charge, 5)
                total_in = now_price * stock_amount - service_charge
                user = dbo.searchOne(UserInformation, UserInformation.user_id, user_id)
                user.free_money_amount += total_in
                holdings.stock_amount -= stock_amount
                dbo.update()
                return "卖出成功\n股票：{}\n股数：{}\n总价格：{}\n当前可支配金额：{}".format(stock_name, str(stock_amount),
                                                                       str(total_in),
                                                                       str(user.free_money_amount))

    @showExpection
    def searchUserHoldings(self, user_id: str) -> str:
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

    @showExpection
    def searchUserInformation(self, user_id: str) -> str:
        dbo = DataBaseOperator()
        user = dbo.searchOne(UserInformation, UserInformation.user_id, user_id)
        if not user:
            return "查询失败，您尚未注册"
        holdings = dbo.searchAllWithField(UserHoldings, UserHoldings.user_id, user_id)
        user.total_money_amount = 0
        for holding in holdings:
            try:
                stock_id = dbo.searchOne(AllStock, AllStock.stock_name, holding.stock_name).stock_id
                price_now = self.getPrice(stock_id)
                user.total_money_amount += holding.stock_amount * price_now
            except:
                return "查询个人信息失败，请稍后重试"
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

    @showExpection
    def help(self):
        s = "使用命令:\n！注册\n" \
            + "！买入 股票名 购买数量\n" + \
            "！卖出 股票名 卖出数量\n！持仓\n！信息\n" \
            + "！查询 股票名\n！K 股票名 天数（绘制倒数K天的K线）\n！c （查询数字货币行情）" + "\n本次更新删除了自选股设计" \
                                                               "，挂单功能停用，在后续更新中维护，敬请期待\n" \
                                                               "感谢您的使用"
        return s

    @showExpection
    def searchOneStock(self, stock_name):
        dbo = DataBaseOperator()
        stocks = dbo.searchLike(AllStock, AllStock.stock_name, '%' + stock_name + '%')
        if len(stocks) == 0:
            return "查询失败，API缺少该股信息"
        elif len(stocks) == 1:
            stock_id = stocks[0].stock_id
            stock_name = stocks[0].stock_name
        elif len(stocks) <= 12:
            rst = "您要找的是不是：\n"
            for i in range(0, len(stocks) - 1):
                rst += stocks[i].stock_name + '\n'
            rst+=stocks[-1].stock_name
            return rst
        else:
            return "模糊匹配的股票数量过多，请指定更精确的股票名"
        df = ts.get_realtime_quotes(stock_id)
        now_price = float(df['price'])
        flush_time = datetime.datetime.strptime(df['date'][0] + " " + df['time'][0], '%Y-%m-%d %H:%M:%S')
        try:
            up_down_rate = 100 * (float(df['price'][0]) - float(df['pre_close'][0])) / float(
                df['pre_close'][0])
        except:
            up_down_rate = 0
        return "{} {} {:.3f}% {}".format(stock_name, now_price,
                                         up_down_rate,
                                         flush_time)

    @showExpection
    def getBTC(self):
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

    @showExpection
    def getCryPto(self):
        try:
            try:
                r = requests.get('https://api.binance.me/api/v3/ticker/price', timeout=3)
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

    @showExpection
    def rank(self):
        try:
            dbo = DataBaseOperator()
            users = dbo.searchAll(UserInformation)
            for i in range(len(users)):
                user = users[i]
                holdings = dbo.searchAllWithField(UserHoldings, UserHoldings.user_id, user.user_id)
                user.total_money_amount = 0
                for holding in holdings:
                    try:
                        stock = dbo.searchOne(AllStock, AllStock.stock_name, holding.stock_name)
                        price_now = self.getPrice(stock.stock_id)
                        if price_now == 0:
                            return "存在个股金额为0，请等待API更新今日价格"
                        user.total_money_amount += holding.stock_amount * price_now
                    except:
                        return "查询个人信息失败:API不稳定，请稍后重试"
                user.total_money_amount += user.free_money_amount
                dbo.update()
            users.sort(reverse=True, key=(lambda user: user.total_money_amount))
            rst = ""
            for i in range(0, len(users)):
                rst += "{}. {} {}\n".format(i + 1, users[i].user_name, users[i].total_money_amount)
            return rst
        except:
            return "连接数据库失败，请稍后重试"

    @showExpection
    def drawK(self, stock_name: str, deltatime: str):
        deltatime = int(deltatime)
        dbo = DataBaseOperator()
        now = datetime.datetime.now().strftime('%Y%m%d')
        last = (datetime.datetime.now() - datetime.timedelta(days=deltatime)).strftime('%Y%m%d')
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

        plt.savefig('E:\\learn\\2103\\SimulationStockBasedOnQQBot\\resource\\go-cqhttp-v0.9.40-fix4-windows-amd64\\data\\images\\Kline.png')
        return True


if __name__ == "__main__":
    server = Server()
    print(server.searchOneStock("我是一只无效的股票名"))
