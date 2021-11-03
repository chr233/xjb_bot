'''
# @Author       : Chr_
# @Date         : 2021-11-02 14:25:11
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-03 13:58:47
# @Description  : 处理投稿
'''

from typing import List
from aiogram.types.message import Message


async def handle_single_post(message: Message):
    await message.reply('111')


async def handle_mulite_post(messages: List[Message]):
    await messages[0].reply('233')
