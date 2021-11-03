'''
# @Author       : Chr_
# @Date         : 2021-10-27 13:12:21
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-03 13:52:40
# @Description  : 
'''

from loguru import logger
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2


from config import CFG, Bot_Modes

from db import init_orm, close_orm

from command.user import setup as user_setup
from command.admin import setup as admin_setup
from chat.post import setup as post_setup

from middleware.user_login import UserLogin


def main():
    '''启动函数'''

    bot = Bot(token=CFG.Bot_Token)

    if not CFG.Mongo:
        if CFG.DEBUG_MODE:
            storge = MemoryStorage()
            logger.warning('Using Memory for storage.')
        else:
            storge = RedisStorage2()
            logger.info('Using Redis for storage.')
    else:
        storge = MongoStorage(uri=CFG.Mongo_URL)
        logger.info('Using Mongo for storage.')
        
    dispatcher = Dispatcher(bot, storage=storge)

    dispatcher.middleware.setup(UserLogin())

    startups = [
        init_orm,
        user_setup,
        admin_setup,
        post_setup,
    ]
    shutdowns = [close_orm]

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
