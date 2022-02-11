'''
# @Author       : Chr_
# @Date         : 2021-10-29 15:42:27
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-12 00:37:05
# @Description  : 用户命令
'''

from loguru import logger
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message

from controller.permission import Permissions, msg_need_permission

from .myinfo import handle_myinfo
from .help import handle_help
from .common import handle_start, handle_version


async def setup(dp: Dispatcher, *args, **kwargs):

    @dp.message_handler(commands=['start'])
    @msg_need_permission(permission=Permissions.Cmd)
    async def _(message: Message):
        await handle_start(message)

    @dp.message_handler(commands=['help'])
    @msg_need_permission(permission=Permissions.Cmd)
    async def _(message: Message):
        await handle_help(message)

    @dp.message_handler(commands=['version'])
    @msg_need_permission(permission=Permissions.Cmd)
    async def _(message: Message):
        await handle_version(message)

    @dp.message_handler(commands=['myinfo'])
    @msg_need_permission(permission=Permissions.Cmd)
    async def _(message: Message):
        await handle_myinfo(message)

    logger.info('User dispatcher loaded')
