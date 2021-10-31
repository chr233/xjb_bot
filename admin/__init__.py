'''
# @Author       : Chr_
# @Date         : 2021-10-29 19:37:40
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-31 16:06:31
# @Description  : 
'''

from loguru import logger
from aiogram import Dispatcher, types

from controller.permission import need_permission,Permissions


from .systop import cmd_systop

from config import CFG

async def setup(dp: Dispatcher, *args, **kwargs):

    @dp.message_handler(commands=['top'])
    @need_permission(permission=Permissions.AdminCmd)
    async def top(message: types.Message):
        user_id = message.from_user.id
        
        if user_id in CFG.Super_Admin:
            await cmd_systop(message)
        else:
            await message.answer("爬")

    logger.info('Admin dispatcher loaded')
