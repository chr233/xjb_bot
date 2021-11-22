'''
# @Author       : Chr_
# @Date         : 2021-11-02 13:26:30
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-22 22:32:41
# @Description  : 重置user_login模块
'''

from aiogram.dispatcher import Dispatcher
from aiogram.types.message import Message

from config import CFG


async def handle_reload(message: Message):

    dispatcher = Dispatcher.get_current()

    user_login = dispatcher.middleware.applications[0]

    user_login.ready = False
    await user_login.prepare_models()

    await message.reply('初始化UserLogin完成')


async def handle_get_chat_id(message: Message):
    bot = message.bot
    ac = await bot.get_chat(chat_id=CFG.Accept_Channel)
    rc = await bot.get_chat(chat_id=CFG.Reject_Channel)
    rg = await bot.get_chat(chat_id=CFG.Review_Group)

    await message.reply((
        f'发布频道: {ac}\n'
        f'拒稿频道: {rc}\n'
        f'审核群组: {rg}\n'
    ))
