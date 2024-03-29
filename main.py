'''
# @Author       : Chr_
# @Date         : 2021-10-27 13:12:21
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-21 13:51:09
# @Description  : 启动入口
'''

from loguru import logger
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from custom.error_handler import error_handler



from config import CFG, Bot_Modes

from db import init_orm, close_orm
from storage import close_storage

from command.user import setup as user_setup
from command.admin import setup as admin_setup
from chat.post import setup as post_setup


from middleware.user_login import UserLogin
from middleware.largest_photo import LargestPhoto
from middleware.log import LoggingMiddleware


def main():
    '''启动函数'''

    bot = Bot(token=CFG.Bot_Token, proxy=CFG.PROXY)

    if CFG.DEBUG_MODE:
        storge = MemoryStorage()
        logger.warning('Using Memory for storage.')
    else:
        storge = RedisStorage2(
            state_ttl=3600, data_ttl=3600, bucket_ttl=3600,
        )
        logger.info('Using Redis for storage.')

    dispatcher = Dispatcher(bot, storage=storge)

    dispatcher.middleware.setup(UserLogin())
    # dispatcher.middleware.setup(LargestPhoto())
    # dispatcher.middleware.setup(LoggingMiddleware())
    # dispatcher.register_errors_handler(error_handler)

    startups = [
        init_orm,
        user_setup,
        admin_setup,
        post_setup,
    ]
    shutdowns = [
        close_orm,
        close_storage,
    ]

    if CFG.Bot_Mode == Bot_Modes.P:
        executor.start_polling(
            dispatcher,
            on_startup=startups,
            on_shutdown=shutdowns
        )
    else:
        executor.start_webhook(
            dispatcher,
            on_startup=startups,
            on_shutdown=shutdowns
        )


if __name__ == '__main__':
    main()
