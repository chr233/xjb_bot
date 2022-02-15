'''
# @Author       : Chr_
# @Date         : 2021-11-02 14:23:19
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-12 19:28:15
# @Description  : 接受投稿
'''

from loguru import logger

from aiogram.dispatcher import filters, Dispatcher

from .message import setup as message_setup
from .queue import setup as queue_setup


async def setup(dp: Dispatcher, *args, **kwargs):
    await message_setup(dp, *args, **kwargs)

    await queue_setup(dp, *args, **kwargs)

    logger.info('Post dispatcher loaded')
