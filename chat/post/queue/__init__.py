'''
# @Author       : Chr_
# @Date         : 2022-02-12 19:24:01
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-17 10:10:34
# @Description  : 处理回调
'''

from aiogram.types import CallbackQuery
from aiogram.dispatcher import  Dispatcher,FSMContext

from controller.permission import  query_need_permission, Permissions


from .submit_post import handle_submit_post_callback
from .direct_post import handle_direct_post_callback
from .review_post import handle_review_post_callback
from .reject_post import handle_reject_post_callback


async def setup(dp: Dispatcher, *args, **kwargs):
    # 投稿回调
    @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('sp_'))
    @query_need_permission(permission=Permissions.Post)
    async def _(callback_query: CallbackQuery):
        await handle_submit_post_callback(callback_query)

    # 直接投稿回调
    @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('dp_'))
    @query_need_permission(permission=Permissions.DirectPost)
    async def _(callback_query: CallbackQuery):
        await handle_direct_post_callback(callback_query)

    # 审核回调
    @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('rp_'))
    @query_need_permission(permission=Permissions.ReviewPost)
    async def _(callback_query: CallbackQuery):
        await handle_review_post_callback(callback_query)

    # 拒稿回调
    @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('jp_'))
    @query_need_permission(permission=Permissions.ReviewPost)
    async def _(callback_query: CallbackQuery):
        await handle_reject_post_callback(callback_query)