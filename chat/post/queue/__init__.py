'''
# @Author       : Chr_
# @Date         : 2022-02-12 19:24:01
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-12 19:31:02
# @Description  : 处理回调
'''


import imp
from typing import List
from loguru import logger
from aiogram.types.message import ContentType, Message
from aiogram.types import CallbackQuery
from aiogram.dispatcher import filters, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter, MediaGroupFilter
from aiogram.dispatcher.handler import CancelHandler

from controller.permission import msg_need_permission, query_need_permission, Permissions
from custom.media_group_handler import media_group_handler
from models.user import Users


from .submit_post import handle_submit_post_callback
from .direct_post import handle_direct_post_callback
from .review_post import handle_review_post_callback


async def setup(dp: Dispatcher, *args, **kwargs):
    # 投稿回调
    @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('sp_'))
    @query_need_permission(permission=Permissions.Post)
    async def _(callback_query: CallbackQuery):
        await handle_submit_post_callback(callback_query)

    # 直接投稿回调
    @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('dp_'))
    @query_need_permission(permission=Permissions.Post)
    async def _(callback_query: CallbackQuery):
        await handle_direct_post_callback(callback_query)

    # 审核回调
    @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('rp_'))
    @query_need_permission(permission=Permissions.ReviewPost)
    async def _(callback_query: CallbackQuery):
        ...
        await handle_review_post_callback(callback_query)
