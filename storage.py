'''
# @Author       : Chr_
# @Date         : 2021-11-03 19:17:40
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-16 12:29:38
# @Description  : 储存池相关
'''

from loguru import logger
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.redis import RedisStorage2


async def close_storage(dp: Dispatcher, *args, **kwargs):
    '''
    关闭储存池
    '''
    storage = dp.storage

    if isinstance(storage, RedisStorage2):
        await storage.close()
        await storage.wait_closed()
        logger.info("Storage closed")
