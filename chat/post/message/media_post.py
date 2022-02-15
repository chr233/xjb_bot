'''
# @Author       : Chr_
# @Date         : 2022-02-12 19:25:26
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-13 11:09:08
# @Description  : 处理媒体类型的稿件
'''


from typing import List
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types.base import InputFile
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.input_media import InputMedia, MediaGroup
from aiogram.types.message import Message, ParseMode
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from buttons.review import RKH, ReviewKeyboardsHelper
from models.base_model import FileObj, SourceLink
from aiogram.utils.exceptions import InvalidQueryID
from aiogram.utils.markdown import escape_md


from models.post import Posts, Post_Status

from buttons.submit import SubmitPostKey, gen_submit_keyboard
from models.user import Users
from utils.emojis import GHOST, NO, SMILE, YES
from utils.largest_media import find_largest_media
from utils.regex_helper import pure_caption
from controller.permission import check_permission, Permissions

from .pre_post import pre_create_new_post

async def handle_media_post(messages:List[Message]):

    if len(messages) == 1:
        await handle_single_post(messages[0])
    else:
        await handle_mulite_post(messages, messages[0].user)
        

async def handle_single_post(message: Message):
    anymouse_mode = message.user.prefer_anymouse

    keyboard = gen_submit_keyboard(anymouse_mode)

    resp = await message.reply('确定要投稿吗？\n\n可以选择是否保留来源', reply_markup=keyboard)

    content_type = message.content_type
    if content_type == 'photo':
        file = find_largest_media(message.photo)
    else:
        media_obj = message[content_type]
        file = FileObj(
            file_id=media_obj.file_id,
            file_uid=media_obj.file_unique_id,
            file_type=content_type,
            file_size=media_obj.file_size,
        )

    await pre_create_new_post(message, resp, [file])


async def handle_mulite_post(messages: List[Message]):
    files = []

    for msg in messages:
        content_type = msg.content_type
        file = find_largest_media(msg[content_type])
        if file:
            files.append(file)

    msg = messages[0]
    user = msg.user

    anymouse_mode = user.prefer_anymouse

    keyboard = gen_submit_keyboard(anymouse_mode)

    resp = await msg.reply('确定要投稿吗？\n\n可以选择是否保留来源', reply_markup=keyboard)

    await pre_create_new_post(msg, resp, files)
