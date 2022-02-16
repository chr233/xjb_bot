'''
# @Author       : Chr_
# @Date         : 2022-02-13 00:28:15
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-16 21:50:05
# @Description  : 准备投稿
'''

from html import escape
from typing import List
from aiogram.types.message import Message
from models.base_model import FileObj, SourceLink


from models.post import Posts, Post_Status

from utils.regex_helper import pure_caption


async def pre_create_new_post(msg: Message, msg2: Message, files: List[FileObj] = None):
    '''
    发布投稿(需要确认后发送至审核频道)
    '''

    if msg.content_type == 'text':
        raw_caption = msg.text
    else:
        raw_caption = msg.caption or ''

    raw_caption = escape(raw_caption)

    if raw_caption:
        caption = pure_caption(raw_caption)
    else:
        caption = ''

    forward_from = msg.forward_from_chat

    user = msg.user

    if forward_from and forward_from.type == 'channel':
        # 如果是频道转发
        forward = True

        msg_id = msg.forward_from_message_id
        mention = forward_from.mention
        source = SourceLink(name=forward_from.full_name,
                            url=f'https://t.me/{mention}/{msg_id}')
    else:
        forward = False
        source = SourceLink(name=user.user_nick, url=user.tg_link())

    if not files:
        files = ''

    await Posts.create(
        origin_mid=msg.message_id,
        action_mid=msg2.message_id,
        review_mid=-msg.message_id,
        manage_mid=-msg2.message_id,
        anymouse=user.prefer_anymouse,
        forward=forward,
        poster=user,
        status=Post_Status.Padding,
        caption=caption,
        raw_caption=raw_caption,
        tags=0,
        source=source,
        files=files
    )
