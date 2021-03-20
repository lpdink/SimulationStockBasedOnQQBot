from nonebot import on_command, CommandSession
from controller.awesome.plugins.Handler import Handler

'''
QQBotPlugins将定义所有的命令处理器，并调用Handler中定义的处理程序进行处理，发送返回结果。
本文件包括所有命令的命令处理器（主程序），参数解析器（如果必要），命令的处理程序将定义在Handler中。
我们通过两种方式获取玩家的信息：
1. 跟随命令给出的参数，例如 ！添加自选股 123456 我们通过命令解析器获取字符串123456，这样就知道玩家想添加哪只股票了。
    多个参数时，我们规定按照空格分割
2. 玩家本身的参数，通过session.event字段读取，规格如下：
'''
'''
这是session.event字段的全部信息，如果使用session.event[self_id]，就能得到123456789的返回值，这是机器人的QQ号
如果使用session.event[sender][nickname]，就能得到顺其自然的返回值，这是向机器人发送消息的（玩家）的昵称
因此，[user_id]字段，或是[sender][user_id]字段，都可以得到玩家的QQ号
这是字典的数据结构，value值可能是任何类型，如果要用作发送的消息，务必通过str()转换
<Event,
 {
 'font': 0, 
 'message': [{'type': 'text', 'data': {'text': '！注册'}}], 
'message_id': -1167733213, 
'message_type': 'private', 
'post_type': 'message',
 'raw_message': '！注册', 
 'self_id': 123456789, 
'sender': {'age': 0, 'nickname': '顺其自然', 'sex': 'unknown', 'user_id': 326490366}, 
'sub_type': 'friend', 
'time': 1616168875,
 'user_id': 326490366, 
 'to_me': True
 }
 >
'''


#####################################################################
# 两个#########分割线间，是一个完整的处理逻辑，即on_command下的命令处理器（定义触发条件，命令的主程序）
# args_parser下的的命令解析器（将跟随命令的参数提取出来）
# handler：命令的处理函数，我们会在Handler中定义。
# 注意，触发了命令，但是没有跟随参数，或者跟随参数的类型不正确，要考虑的因素过多，因此在命令的主程序中，统一:
# try:
#   function()
# except:
#   pass

# on_command 装饰器将函数声明为一个命令处理器
# 这里 测试 为命令的名字，同时允许使用别名test
@on_command('测试', aliases=('test'))
async def test(session: CommandSession):
    # 从会话状态（session.state）中获取用户传递的参数
    args = session.get('args')  # , prompt='你想查询哪个城市的天气呢？')
    # 调用处理函数
    if args != "":
        response = await test_handler(args)
        # 发送处理函数的返回值
        await session.send(response)


# test.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@test.args_parser
async def test_args_parser(session: CommandSession):
    # 去掉消息首尾的空白符，注意这不包括命令本身
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['args'] = stripped_arg
    else:
        session.state['args'] = ""


# 这是命令test的处理程序，我们会在Handler.py中定义所有的处理程序，而不是在本文件中
async def test_handler(args: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该返回处理结果
    return f"我是参数{args}的处理结果"


#########################################################
# 注册
# 命令格式：！注册
@on_command('注册', aliases=('register'))
async def register(session: CommandSession):
    try:
        handler = Handler()
        user_id = str(session.event['sender']['user_id'])
        user_name = str(session.event['sender']['nickname'])
        response = handler.register(user_id, user_name)
        await session.send(str(response))
    except:
        pass


# 添加自选股
# 命令格式：!添加自选股 123456
@on_command('添加自选股', aliases=('addSelfStock'))
async def addSelfStock(session: CommandSession):
    try:
        stock_id = session.get('stock_id')
        handler = Handler()
        response = handler.addSelfStock(stock_id)
        await session.send(str(response))
    except:
        pass


@addSelfStock.args_parser
async def addSelfStockArgsParser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['stock_id'] = stripped_arg
    else:
        raise Exception('添加自选股命令缺少参数')


# 购买股票
# 命令格式：！购买股票 股票编号 购买价格 购买数量
@on_command('购买股票', aliases=('buyStock'))
async def buyStock(session: CommandSession):
    try:
        user_id = str(session.event['sender']['user_id'])
        stock_id = session.get('stock_id')
        stock_price = session.get('stock_price')
        stock_amount = session.get('stock_amount')
        handler = Handler()
        response = handler.buyStock(user_id, stock_id, stock_amount, stock_price)
        await session.send(str(response))
    except:
        pass


@buyStock.args_parser
async def buyStockArgsParser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        args = stripped_arg.split()
        session.state['stock_id'] = args[0]
        session.state['stock_price'] = args[1]
        session.state['stock_amount'] = args[2]
    else:
        raise Exception('购买股票命令缺少参数')


# 卖出股票
# 命令格式：！卖出股票 股票编号 卖出价格 卖出数量
@on_command('卖出股票', aliases=('sellStock'))
async def sellStock(session: CommandSession):
    try:
        user_id = str(session.event['sender']['user_id'])
        stock_id = session.get('stock_id')
        stock_price = session.get('stock_price')
        stock_amount = session.get('stock_amount')
        handler = Handler()
        response = handler.sellStock(user_id, stock_id, stock_amount, stock_price)
        await session.send(str(response))
    except:
        pass


@sellStock.args_parser
async def sellStockArgsParser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        args = stripped_arg.split()
        session.state['stock_id'] = args[0]
        session.state['stock_price'] = args[1]
        session.state['stock_amount'] = args[2]
    else:
        raise Exception('卖出股票命令缺少参数')


# 查询持仓
# 命令格式：!查询持仓
@on_command('查询持仓', aliases=('searchUserHoldings'))
async def searchUserHoldings(session: CommandSession):
    try:
        user_id = str(session.event['sender']['user_id'])
        handler = Handler()
        response = handler.searchUserHoldings(user_id)
        await session.send(str(response))
    except:
        pass


# 查询订单
# 命令格式：!查询订单
@on_command('查询订单', aliases=('searchAliveOrders'))
async def searchAliveOrders(session: CommandSession):
    try:
        user_id = str(session.event['sender']['user_id'])
        handler = Handler()
        response = handler.searchAliveOrders(user_id)
        await session.send(str(response))
    except:
        pass


# 查询玩家信息
# 命令格式：!我的信息
@on_command('我的信息', aliases=('searchUserInformation'))
async def searchUserInformation(session: CommandSession):
    try:
        user_id = str(session.event['sender']['user_id'])
        handler = Handler()
        response = handler.searchUserInformation(user_id)
        await session.send(str(response))
    except:
        pass


# 取消订单
# 命令格式：！取消订单 订单id
@on_command('取消订单', aliases=('cancelOrder'))
async def cancelOrder(session: CommandSession):
    try:
        user_id = str(session.event['sender']['user_id'])
        order_id = session.get('order_id')
        handler = Handler()
        response = handler.cancelOrder(user_id, order_id)
        await session.send(str(response))
    except:
        pass


@cancelOrder.args_parser
async def cancelOrderArgsParser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['order_id'] = stripped_arg
    else:
        raise Exception('取消订单命令缺少参数')
