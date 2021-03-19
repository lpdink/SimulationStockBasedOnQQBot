from os import path
import nonebot
import controller.config

if __name__ == '__main__':
    nonebot.init(controller.config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'awesome', 'plugins'),
        'awesome.plugins'
    )
    nonebot.run()
