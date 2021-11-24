'''
# @Author       : Chr_
# @Date         : 2021-11-02 14:23:19
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-24 23:17:22
# @Description  : 接受投稿
'''


from typing import List
from loguru import logger
from aiogram.types.message import ContentType, Message
from aiogram.types import CallbackQuery
from aiogram.dispatcher import filters, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter, MediaGroupFilter

from controller.permission import msg_need_permission, query_need_permission, Permissions
from custom.media_group_handler import media_group_handler
from models.user import Users

from .submit_post import handle_submit_post_callback, handle_text_message, handle_single_post, handle_mulite_post
from .review_post import handle_review_post_callback


async def setup(dp: Dispatcher, *args, **kwargs):
    # 投稿回调
    @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('sp_'))
    @query_need_permission(permission=Permissions.Post)
    async def _(callback_query: CallbackQuery):
        await handle_submit_post_callback(callback_query)

    # 审核回调
    @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('rp_'))
    @query_need_permission(permission=Permissions.Review)
    async def _(callback_query: CallbackQuery):
        ...
        await handle_review_post_callback(callback_query)

    # 投稿消息处理
    @dp.message_handler(ChatTypeFilter('private'), content_types=ContentType.TEXT)
    @msg_need_permission(permission=Permissions.Cmd)
    async def _(message: Message):
        await handle_text_message(message)

    @dp.message_handler(ChatTypeFilter('private'), MediaGroupFilter(False), content_types=ContentType.ANY)
    @msg_need_permission(permission=Permissions.Post)
    async def _(message: Message):
        await handle_single_post(message)

    @dp.message_handler(ChatTypeFilter('private'), filters.MediaGroupFilter(True), content_types=ContentType.ANY)
    @msg_need_permission(permission=Permissions.Post)
    @media_group_handler()
    async def _(messages: List[Message], user: Users):
        await handle_mulite_post(messages, user)

    logger.info('Post dispatcher loaded')
