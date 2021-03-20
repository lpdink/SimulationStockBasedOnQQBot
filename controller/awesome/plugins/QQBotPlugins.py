from nonebot import on_command, CommandSession

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