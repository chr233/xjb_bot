'''
# @Author       : Chr_
# @Date         : 2021-11-02 13:26:30
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-02 14:09:38
# @Description  : 重置user_login模块
'''

from aiogram.dispatcher import Dispatcher
from aiogram.types.message import Message


async def handle_reload(message: Message):

    dispatcher = Dispatcher.get_current()

    user_login = dispatcher.middleware.applications[0]

    user_login.ready = False
    await user_login.prepare_models()

    await message.reply('初始化UserLogin完成')
