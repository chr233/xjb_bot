'''
# @Author       : Chr_
# @Date         : 2021-10-29 15:42:27
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-17 09:45:42
# @Description  : 用户命令
'''

from loguru import logger
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message

from controller.permission import Permissions, msg_need_permission

from .myinfo import handle_myinfo
from .help import handle_help
from .veriosn import handle_start, handle_version
from .cancel import handle_cancel


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
        
    @dp.message_handler(state='*', commands='cancel')
    @msg_need_permission(permission=Permissions.Cmd)
    async def _(message:Message,state:FSMContext):
        await handle_cancel(message,state)

    logger.info('User dispatcher loaded')
