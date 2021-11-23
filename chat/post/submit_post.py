'''
# @Author       : Chr_
# @Date         : 2021-11-02 14:25:11
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-24 00:12:04
# @Description  : 处理投稿
'''

from typing import List
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from buttons.review import RKH, ReviewKeyboardsHelper
from models.base_model import FileObj, SourceLink
from aiogram.utils.exceptions import InvalidQueryID

from models.post import Posts, Post_Status

from buttons.submit import SubmitPostKey, gen_submit_keyboard
from utils.emojis import GHOST, NO, SMILE
from utils.regex_helper import pure_caption

from config import CFG


async def submit_new_post(message: Message):
    ...


async def handle_submit_post_callback(query: CallbackQuery):
    '''
    处理投稿按钮回调
    '''
    data = query.data
    bot = query.bot

    chat_id = query.message.chat.id
    msg_id = query.message.message_id

    user = query.user

    if 'anymouse_' in data:
        anymouse = data == SubmitPostKey.anymouse_on

        kbd = gen_submit_keyboard(anymouse)

        await query.answer('已开启匿名模式' if anymouse else '已关闭匿名模式',)
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=msg_id, reply_markup=kbd)
    else:
        post = await Posts.get_or_none(action_mid=msg_id)

        if not post:
            await query.answer('投稿不存在')
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text='投稿不存在',
            )
            return

        # if post.poster.user_id != user.user_id:
        #     await query.answer('仅限本人操作')
        #     return

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
                        f'投稿人: {post.poster.md_link}'
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
                        f'稿件状态: {str(Post_Status.Reviewing)}\n'
                        f'采用数/总投稿: {user.accept_count}/{user.post_count}'
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


async def create_new_post(msg: Message, msg2: Message):
    '''
    发布投稿
    '''
    raw_caption = msg.text
    if raw_caption:
        caption = pure_caption(raw_caption)
    else:
        raw_caption = caption = ''

    if 'NSFW' in raw_caption.upper():
        tags = 'NSFW'
    else:
        tags = ''

    forward_from = msg.forward_from_chat

    if forward_from and forward_from.type == 'channel':
        # 如果是频道转发
        msg_id = msg.forward_from_message_id
        mention = forward_from.mention
        source = SourceLink(name=forward_from.full_name,
                            url=f'https://t.me/{mention}/{msg_id}')
    else:
        source = ''

    content_type = msg.content_type

    if content_type != 'text':
        files = []

        medias = msg[content_type]

        if content_type == 'photo':
            medias = medias[-1:]

        for media in medias:
            files .append(
                FileObj(
                    file_id=media.file_id,
                    file_uid=media.file_unique_id,
                    file_size=media.file_size,
                    height=media.height,
                    width=media.width
                )
            )
    else:
        files = ''

    await Posts.create(
        origin_mid=msg.message_id,
        action_mid=msg2.message_id,
        review_mid=-msg.message_id,
        manage_mid=-msg2.message_id,
        anymouse_mode=False,
        poster=msg.user,
        status=Post_Status.Padding,
        caption=caption,
        raw_caption=raw_caption,
        tags=tags,
        source=source,
        files=files
    )


async def handle_text(message: Message):
    # await message.reply('暂不支持文字投稿哟~')
    # raise CancelHandler()

    anymouse_mode = message.user.prefer_anymouse

    keyboard = gen_submit_keyboard(anymouse_mode)

    resp = await message.reply('确定要投稿吗？\n\n可以选择是否保留来源', reply_markup=keyboard)

    await create_new_post(message, resp)


async def handle_single_post(message: Message):
    anymouse_mode = message.user.prefer_anymouse

    keyboard = gen_submit_keyboard(anymouse_mode)

    resp = await message.reply('确定要投稿吗？\n\n可以选择是否保留来源', reply_markup=keyboard)

    await create_new_post(message, resp)


async def handle_mulite_post(messages: List[Message]):
    await messages[0].reply('233')
