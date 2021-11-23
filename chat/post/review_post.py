'''
# @Author       : Chr_
# @Date         : 2021-11-02 14:25:18
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-24 00:38:49
# @Description  : 审核投稿
'''

from typing import List
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.input_media import MediaGroup
from aiogram.types.message import Message
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from buttons.review import RKH, ReviewKeyboardsHelper, ReviewPostKey
from models.base_model import FileObj, SourceLink
from aiogram.utils.exceptions import InvalidQueryID

from models.post import Posts, Post_Status

from buttons.submit import SubmitPostKey, gen_submit_keyboard

from config import CFG
from utils.emojis import NO, YES


async def handle_review_post_callback(query: CallbackQuery):
    data = query.data
    bot = query.bot

    chat_id = query.message.chat.id
    msg_id = query.message.message_id

    user = query.user

    try:
        cmd, selected = data.split(' ')
        tags = int(selected)
    except ValueError:
        cmd = data.strip()
        tags = 0
        # return

    post = await Posts.get_or_none(manage_mid=msg_id)

    if not post:
        await query.answer('投稿不存在')
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text='投稿不存在',
        )
        return

    if cmd == ReviewPostKey.accept:
        tags = RKH.get_tag(tags)

        await query.answer('已发布')
        
        # await bot.edit_message_ca(
        # )
        
        await bot.forward_message()
        
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=(
                f'投稿人: {post.poster.md_link}\n'
                f'匿名: {YES if post.anymouse else NO}\n'
                f'审核人: {user.md_link}'
                f'状态: {Post_Status.Accepted}'
            )
        )

    elif cmd == ReviewPostKey.reject:
        post = await Posts.get_or_none(action_mid=msg_id)

        if not post:
            await query.answer('投稿不存在')
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text='投稿不存在',
            )
            return

        if data == SubmitPostKey.cancel:
            await query.answer('投稿已取消')
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text='投稿已取消',
            )
            post.update_from_dict({
                'caption': '',
                'status': Post_Status.Cancel,
                'source': '',
                'files': '',
            })

        elif '_post' in data:
            user = query.user
            if post.status == Post_Status.Padding:
                anymouse = data == SubmitPostKey.post_anymouse

                review_mid = await bot.forward_message(
                    chat_id=CFG.Review_Group,
                    from_chat_id=chat_id,
                    message_id=post.origin_mid
                )

                keyboard = await RKH.get_tag_keyboard_short(0)

                manage_mid = await bot.send_message(
                    chat_id=CFG.Review_Group,
                    text=(
                        f'投稿来源: {str(post.poster)}'
                    ),
                    reply_markup=keyboard
                )

                post.update_from_dict({
                    'status': Post_Status.Reviewing,
                    'anymouse': anymouse,
                    'review_mid': review_mid,
                    'manage_mid': manage_mid
                })

                await query.answer('稿件投递成功')

                user.post_count += 1

                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=msg_id,
                    text=(
                        f'稿件状态: `{Post_Status.Reviewing}`\n'
                        f'采用数/总投稿: `{user.accept_count}/{user.post_count}`'
                    )
                )

                await user.save()

            else:
                await query.answer('请不要重复提交')
                await bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=msg_id
                )
        else:
            await query.answer('未知操作')
            return

        await post.save()

    data = query.data
    msg_id = query.message.message_id

    print(data, msg_id)
