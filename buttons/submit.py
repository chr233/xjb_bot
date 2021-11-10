'''
# @Author       : Chr_
# @Date         : 2021-11-03 19:46:39
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-10 14:55:09
# @Description  : 
'''


import asyncio
import logging
from datetime import datetime
from operator import itemgetter

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardButton as IKButon

from utils.strings import bool2str
from utils.emojis import GHOST, SMILE, NO, YES


__submit_post_kbd = [
    [IKButon(f'{SMILE}保留来源', callback_data='anymouse_mode')],
    [IKButon(f'{NO}取消', callback_data='cancal_post'),
     IKButon(f'{YES}投稿', callback_data='submit_post')]
]

__submit_post_kbd = [
    [IKButon(f'{GHOST}匿名投稿', callback_data='anymouse_mode_anymouse')],
    [IKButon(f'{NO}取消', callback_data='cancal_post_anymouse'),
     IKButon(f'{YES}投稿', callback_data='submit_post_anymouse')]
]


def gen_submit_keyboard(anymouse: bool = False):
    keyboard = __submit_post_kbd

    keyboard[0][0].text = f'{GHOST}匿名投稿' if anymouse else f'{SMILE}保留来源'

    return keyboard
