'''
# @Author       : Chr_
# @Date         : 2021-11-02 14:23:19
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-03 15:04:08
# @Description  : 接受投稿
'''


from loguru import logger
from aiogram.types.message import ContentType
from aiogram import Dispatcher, types
from aiogram.dispatcher import filters

from .submit_post import handle_single_post, handle_mulite_post


async def setup(dp: Dispatcher, *args, **kwargs):

    @dp.message_handler(filters.MediaGroupFilter(False), content_types=ContentType.ANY)
    async def _(message: types.Message):
        await handle_single_post(message)

    @dp.message_handler(filters.MediaGroupFilter(True), content_types=ContentType.ANY)
    async def _(message: types.Message):
        await handle_mulite_post([message])

    logger.info('Post dispatcher loaded')
