'''
# @Author       : Chr_
# @Date         : 2021-10-29 19:37:40
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-22 23:27:01
# @Description  : 管理员命令
'''

from loguru import logger
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import Message

from controller.permission import need_permission, Permissions

from .reload import handle_get_chat_id, handle_reload
from .systop import handle_top


async def setup(dp: Dispatcher, *args, **kwargs):

    @dp.message_handler(commands=['top'])
    @need_permission(permission=Permissions.AdminCmd)
    async def _(message: Message):
        await handle_top(message)

    @dp.message_handler(commands=['reload'])
    @need_permission(permission=Permissions.SuperCmd)
    async def _(message: Message):
        await handle_reload(message)
        
    @dp.message_handler(commands=['chatid'])
    @need_permission(permission=Permissions.SuperCmd)
    async def _(message: Message):
        await handle_get_chat_id(message)

    logger.info('Admin dispatcher loaded')
