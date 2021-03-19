from nonebot import on_command, CommandSession


# on_command 装饰器将函数声明为一个命令处理器
# 这里 测试 为命令的名字，同时允许使用别名test
@on_command('测试', aliases=('test'))
async def test(session: CommandSession):
    # 从会话状态（session.state）中获取用户传递的参数
    args = session.get('args')  # , prompt='你想查询哪个城市的天气呢？')
    # 调用处理函数
    if args!="":
        response = await handler(args)
        # 发送处理函数的返回值
        await session.send(response)


# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@test.args_parser
async def test_args_parser(session: CommandSession):
    # 去掉消息首尾的空白符，注意这不包括命令本身
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['args'] = stripped_arg
    else:
        session.state['args'] = ""


async def handler(args: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该返回处理结果
    return f"我是参数{args}的处理结果"

#########################################################
# on_command 装饰器将函数声明为一个命令处理器
# 这里 测试 为命令的名字，同时允许使用别名test
@on_command('注册', aliases=('register'))
async def register(session: CommandSession):
    await session.send(str(session.event['sender']['nickname'])+str(session.event['sender']['user_id']))