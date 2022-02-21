'''
# @Author       : Chr_
# @Date         : 2022-02-12 19:23:56
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-20 21:21:19
# @Description  : 处理消息
'''

from typing import List
from loguru import logger
from aiogram.types.message import ContentType, Message
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter, MediaGroupFilter
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.storage import FSMContext

from .reject_reason import handle_custom_reject_reason
from .file_post import handle_file_post
from .media_post import handle_media_post
from .text_post import handle_text_message


from controller.permission import msg_need_permission, Permissions
from custom.media_group_handler import media_group_handler
from states.reject_reason import RejectForm


async def setup(dp: Dispatcher, *args, **kwargs):

    # 处理自定义拒稿原因
    @dp.message_handler(state=RejectForm.reason, content_types=ContentType.TEXT)
    @msg_need_permission(permission=Permissions.ReviewPost)
    async def _(message: Message, state: FSMContext):
        await handle_custom_reject_reason(message)

    # 处理文字消息处理
    @dp.message_handler(ChatTypeFilter('private'), content_types=ContentType.TEXT)
    @msg_need_permission(permission=Permissions.Post)
    async def _(message: Message):
        if message.text.startswith('/'):
            await message.reply('未知命令, 请使用 /help 查看帮助')
            raise CancelHandler()

        await handle_text_message(message)

    # 处理媒体的消息
    @dp.message_handler(ChatTypeFilter('private'), MediaGroupFilter(False), content_types=ContentType.ANY)
    @msg_need_permission(permission=Permissions.Post)
    async def _(message: Message):
        content_type = message.content_type

        if content_type in ['video', 'voice', 'photo']:
            await handle_media_post([message])
        elif content_type == 'document':
            await handle_file_post([message])
        else:
            logger.info(f'媒体类型: {content_type}')
            await message.reply('未知媒体类型')
            raise CancelHandler()

    # 处理媒体组消息
    @dp.message_handler(ChatTypeFilter('private'), MediaGroupFilter(True), content_types=ContentType.ANY)
    @msg_need_permission(permission=Permissions.Post)
    @media_group_handler()
    async def _(messages: List[Message]):
        if not messages:
            logger.warning('空的 media_group')
            raise CancelHandler()

        msg = messages[0]
        content_type = msg.content_type

        if len(messages) < 2:
            logger.warning('media_group 中只有一个媒体')

        if content_type in ['video', 'voice', 'photo']:
            await handle_media_post(messages)
        elif content_type == 'document':
            await handle_file_post(messages)
        else:
            logger.info(f'媒体类型: {content_type}')
            await msg.reply('暂不支持的投稿类型')
            raise CancelHandler()
