'''
# @Author       : Chr_
# @Date         : 2021-11-02 13:26:30
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-11 23:43:13
# @Description  : 重置user_login模块
'''

from aiogram.dispatcher import Dispatcher
from aiogram.types.message import Message, ParseMode
from aiogram.types import Chat

from config import CFG


async def handle_reload(message: Message):

    dispatcher = Dispatcher.get_current()

    user_login = dispatcher.middleware.applications[0]

    user_login.ready = False
    await user_login.prepare_models()

    await message.answer('初始化UserLogin完成')


def md_link(chat: Chat) -> str:
    return f'[{chat.title} @{chat.username}](https://t.me/{chat.username})'


async def handle_get_chat_id(message: Message):
    bot = message.bot
    ac = await bot.get_chat(chat_id=CFG.Accept_Channel)
    rc = await bot.get_chat(chat_id=CFG.Reject_Channel)
    rg = await bot.get_chat(chat_id=CFG.Review_Group)

    await message.reply(
        text=(
            f'发布频道: {md_link(ac)}\n'
            f'拒稿频道: {md_link(rc)}\n'
            f'审核群组: {md_link(rg)}\n'
        ),
        parse_mode=ParseMode.MARKDOWN_V2)
