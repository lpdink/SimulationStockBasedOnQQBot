# 基于QQBot的模拟炒股方案
----
## 设计
- 流程设计：
	- 玩家在QQ群中，以一定的语法，选择购入、卖出股票，查看股票，账户信息，增设自选股等。
	- 在开盘时间，股票价格每隔5Min刷新一次，玩家买入卖出的操作，也仅在刷新时结算。
	- 若在下一次价格刷新时，玩家选择购入股票的价格高于实际价格，则购入成功，否则持续等待。
	- 若在下一次价格刷新时，玩家选择卖出股票的价格低于实际价格，则卖出成功，否则持续等待。
	- 无论是买入或是卖出，玩家都可以在订单未达成时查看，取消订单。取消订单的操作立即结算。
	- 买入或卖出需要按照当下市场规则，收取一定的手续费。被取消的订单不收取手续费。
- 交互设计
	- 注册：通过!#register 命令授权注册，以玩家QQ号作为uid，进行各项操作，向user_information表中插入新项即可。
	- 添加自选股:通过!#stock + #股票编号，添加自选股。此后，系统开始获取该股票信息。（玩家只能购买或卖出自选股表中的股票）
	- 买入：通过!#buy+股票编号+数量 创建购买订单
	- 卖出：通过!#sell+股票编号+数量 创建卖出订单
	- 查看: 通过!#+search+表名+属性名，查看自选股，个人账户，活跃订单等信息。
	- 取消订单：通过!#+delete+订单编号，删除订单
	- 其他
- 数据设计（表）：
	- 玩家信息(user_information)
		- qq号(user_id)
		- 昵称(user_name)
		- 账户可支配金额(free\_money_amount)
		- 账户总金额(total\_money_amount)
		- 历史总金额(history\_money_amount)
	- 股票信息(stock_information)
		- 股票编号(stock_id)
		- 最后一次刷新价格(now_price)
		- 最后一次刷新时间(flush_time)
		- 历史价格(history_price)
	- 玩家持仓(user_holdings)
		- qq号(user_id)
		- 股票编号(stock_index)
		- 持有数量(stock_amount)
		- 买入时价格(bought_price)
		- 买入订单总价格(bought\_total_price)
	- 活跃订单（alive_orders）
		- qq号(user_id)
		- 活跃订单编号(alive\_order_index)
		- 订单时间(alive\_order_time)
		- 买入/卖出(buy_or_sell)：买入为1，卖出为-1
		- 购买/卖出股票的编号(stock_index)
		- 购买/卖出股票的名称(stock_name)
		- 购买/卖出股票的数量(stock_amount)
		- 购买/卖出股票的单价(stock_price)
		- 订单总金额(order\_money_amount)
	- 全局变量(global_vars)
		- 买入手续费用(buy\_service_charge)
		- 卖出手续费用(sell\_service_charge)
		- 其他
	- 其他
- 模块设计
	- dao:与数据库交互，不考虑前端逻辑
	- domain:与dao交互，只存储信息的基本类，只有属性。
	- service：处理业务逻辑
	- controller：与前端交互，即QQBot的调用部分。

## 实现
 
- dao
	- DataBaseOperator.py
		- 类的属性
			- __connect: 与数据库的连接
			- __cursor: 游标，进行数据库操作
		- 类的方法
			- openConnect(self): 打开数据库连接，创建游标
			- getConnect(self): 获取数据库连接
			- getCursor(self): 获取游标
			- closeConnect(self): 关闭数据库连接，关闭游标
			- addRecord(self, table, record):向表table(str)中插入记录record(str)
			- deleteRecord(self, table, primary_key):从表table(str)中删除主键(id)为primary_key(str)的记录
			- changeRecord(self, table, primary_key, record):将表table(str)中主键（id)为primary_key(str)的记录，修改为record
			- searchRecord(self, table, primary_key, record):返回表table(str)中主键(id)为primary_key的记录
	- dataBaseConfig.ini
		- 数据库的配置文件
- domain
	- 包含的文件
		- 包含的类
			- 类的方法
			- 类的属性
- service
	- 包含的文件
		- 包含的类
			- 类的方法
			- 类的属性
- controller
	- 包含的文件
		- 包含的类
			- 类的方法
			- 类的属性
## TODO
- 【已完成】./dao/DataBaseOperator.py，请帮助完成增删改查函数，实现后务必进行测试，保证与mysql数据库的正常交互，请不要删掉测试用例。
- 【已完成】./domain/，请参考UserInformation.py定义，及readme.md的数据设计部分，完成其余4个类的代码
- ./domain/，参考UserInformation.py中对\__str\__方法的重写，以及readme.md的定义，重写其他四个类的\__str__方法，保证与数据库一条记录的字符串格式一致，能被addrecord方法直接添加。
- ./dao/DataBaseOperator.py,请帮助完成新添加的两个函数searchRecordValue()及searchRecordWithTwoFieldsValue()，具体说明见文件.
- ./service/Server.py，请参考已经实现的register(),addSelfStock(),buyStock()三个方法，完成剩余5个方法的实现。
- 【新增】./dao/DataBaseOperator.py，由于Server.py的需要，请帮助完成新添加的两个函数，deleteRecordWithTwoFields()及 searchRecordWithTwoFields()，具体说明见文件。
## 需要注意的
- 2021-03-19 18：40 xzy
	- 我修改了活跃订单（alive_orders)在readme和domain中的定义，以判断是买入或是卖出订单。
- 2021-03-20 11：01 rky
    - 调整./domain/AliveOrder命名，AliveOrders -> AliveOrder
## 使用框架
- python==3.7（请注意，这是必须的，nonebot要求3.7及以上的版本）
- PyMySQL==1.0.2
- nonebot==1.8.2 [官方文档](https://docs.nonebot.dev/guide/)
- go-cqhttp==v0.9.40 [官方文档](https://docs.go-cqhttp.org/guide/quick_start.html)
## 关于QQBot的配置
- 概述
	- go-cqhttp：本体是一个可执行文件（exe），做好配置，打开后将创建api服务器，socket服务器和http服务器。它将模拟登录我们的QQ号（机器人），通过一定命令，向api服务器发送HTTP请求，我们可以操纵机器人完成发送消息，删除好友等任务。它本身也会接收机器人接收到的消息，并按照我们的配置，转发到处理程序（python程序），这正是我们需要的。
	- nonebot：用于go-cphttp转发的消息，本身也对go-cphttp的api进行了封装，使得我们一方面能收到机器人QQ号收到的消息，另一方面，不必手写HTTP请求，就能通过go-cqhttp完成机器人操作。
- 配置go-cqhttp
	- 建议参考[官方文档](https://docs.go-cqhttp.org/guide/quick_start.html)和本readme共同配置。
	- 访问[go-cqhttp-releases](https://github.com/Mrs4s/go-cqhttp/releases)下载最新版（V0.9.40）windows64位的压缩包。
	- 解压缩包，得到一个go-cqhttp.exe的文件
	- 运行该文件，此时在同目录下，会生成config.hjson配置文件
	- 用文本编辑器打开配置文件，需要编辑：
		- uin: 用作机器人的QQ号
		- password：QQ号的密码
		- encrypt_password：是否对密码加密
		- enable_db: 设置为true
		- heartbeat_interval：建议设置为-1
		- ws\_reverse\_servers:这是关键！go-cqhttp通过这里的配置，知道将消息转发给谁。设置enabled为true，reverse_url为ws://127.0.0.1:8080/ws/，其余不变。
	- 运行go-cqhttp，按照提示操作。
	- 如果遇到需要验证码（滑块）的问题，参考[官方文档-滑块验证码](https://docs.go-cqhttp.org/faq/slider.html)，请选择方案A自行抓包。注意复制ticket时不要复制两端的引号。
	- 运行成功后，你可以尝试通过另一个QQ号向机器人的QQ号发送消息，可以在cqhttp中看到响应。
- 配置none-bot：
	- 通过pip安装none-bot的1.8.2版本（最新版本）
	- 运行./controller/QQBot.py
	- 先打开nonebot或是go-cqhttp都可以，如果成功，可以在nonebot的python命令行里，看到go-cqhttp转发的消息，你依然可以通过上面提到的方法进行测试。
	- 注意，请保证QQBot.py中第六行，host和port的设置与go-cphttp的反向服务器（ws\_reverse\_servers）配置一致.
