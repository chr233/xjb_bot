'''
# @Author       : Chr_
# @Date         : 2021-10-29 19:37:40
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-02 13:31:22
# @Description  : 
'''

from loguru import logger
from aiogram import Dispatcher, types

from controller.permission import need_permission, Permissions

from .reload import handle_reload
from .systop import handle_top


async def setup(dp: Dispatcher, *args, **kwargs):

    @dp.message_handler(commands=['top'])
    @need_permission(permission=Permissions.AdminCmd)
    async def top(message: types.Message):
        await handle_top(message)

    @dp.message_handler(commands=['reload'])
    @need_permission(permission=Permissions.SuperCmd)
    async def reload(message: types.Message):
        await handle_reload(message)

    logger.info('Admin dispatcher loaded')
