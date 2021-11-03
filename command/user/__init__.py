'''
# @Author       : Chr_
# @Date         : 2021-10-29 15:42:27
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-03 00:45:34
# @Description  : 用户命令
'''

from loguru import logger
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message

from .user_info import handle_info
from .help import handle_start, handle_help, handle_version


async def setup(dp: Dispatcher, *args, **kwargs):

    @dp.message_handler(commands=['start'])
    async def _(message: Message):
        await handle_start(message)

    @dp.message_handler(commands=['help'])
    async def _(message: Message):
        await handle_help(message)

    @dp.message_handler(commands=['version'])
    async def _(message: Message):
        await handle_version(message)

    @dp.message_handler(commands=['myinfo'])
    async def _(message: Message):
        await handle_info(message)

    logger.info('User dispatcher loaded')
