'''
# @Author       : Chr_
# @Date         : 2021-11-03 19:46:39
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-03 21:52:23
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


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# some code

_keyboard = [
    [KeyboardButton('Fine')],
    [KeyboardButton('Not bad')],
]
# keyboard = types.ReplyKeyboardMarkup(keyboard=_keyboard)

# await message.reply("Hi!\nHow are you?", reply_markup=keyboard)


studyboi = InlineKeyboardButton('测试', url='https://vk.com/feed')
start_keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(studyboi)
