'''
# @Author       : Chr_
# @Date         : 2021-10-29 15:42:27
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-29 19:17:17
# @Description  : 
'''

from loguru import logger
from aiogram import Dispatcher, types

from .user_info import myInfo


async def setup(dp: Dispatcher, *args, **kwargs):

    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        await myInfo(message)



    logger.info('User dispatcher loaded')