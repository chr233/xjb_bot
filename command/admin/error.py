'''
# @Author       : Chr_
# @Date         : 2021-11-22 21:10:05
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-22 21:10:05
# @Description  : 工具命令
'''

from aiogram.dispatcher import Dispatcher
from aiogram.types.message import Message

async def handle_get_chat_id(message: Message):

    dispatcher = Dispatcher.get_current()

    user_login = dispatcher.middleware.applications[0]

    user_login.ready = False
    await user_login.prepare_models()

    await message.reply('初始化UserLogin完成')
