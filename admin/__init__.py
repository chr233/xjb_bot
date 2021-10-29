'''
# @Author       : Chr_
# @Date         : 2021-10-29 19:37:40
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-29 20:00:51
# @Description  : 
'''

from loguru import logger
from aiogram import Dispatcher, types

from config import CFG

from .systop import cmd_systop


async def setup(dp: Dispatcher, *args, **kwargs):

    @dp.message_handler(commands=['top'])
    async def top(message: types.Message):
        user_id = message.from_user.id
        
        if user_id in CFG.Super_Admin:
            await cmd_systop(message)
        else:
            await message.answer("爬")

    logger.info('Admin dispatcher loaded')
