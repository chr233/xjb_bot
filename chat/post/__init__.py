'''
# @Author       : Chr_
# @Date         : 2021-11-02 14:23:19
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-22 22:40:53
# @Description  : 接受投稿
'''


from loguru import logger
from aiogram.types.message import ContentType, Message
from aiogram.types import CallbackQuery
from aiogram.dispatcher import filters, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter, MediaGroupFilter

from controller.permission import need_permission, Permissions

from .submit_post import handle_submit_post_callback, handle_text, handle_single_post, handle_mulite_post


async def setup(dp: Dispatcher, *args, **kwargs):
    @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('sp_'))
    @need_permission(permission=Permissions.Post)
    async def _(callback_query: CallbackQuery):
        await handle_submit_post_callback(callback_query)

    @dp.message_handler(ChatTypeFilter('private'), content_types=ContentType.TEXT)
    async def _(message: Message):
        await handle_text(message)

    @dp.message_handler(ChatTypeFilter('private'), MediaGroupFilter(False), content_types=ContentType.ANY)
    @need_permission(permission=Permissions.Post)
    async def _(message: Message):
        await handle_single_post(message)

    @dp.message_handler(ChatTypeFilter('private'), filters.MediaGroupFilter(True), content_types=ContentType.ANY)
    @need_permission(permission=Permissions.Post)
    async def _(message: Message):
        await handle_mulite_post([message])

    logger.info('Post dispatcher loaded')
