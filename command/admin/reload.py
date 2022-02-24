'''
# @Author       : Chr_
# @Date         : 2021-11-02 13:26:30
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-21 19:10:17
# @Description  : 重置user_login模块
'''

from aiogram.dispatcher import Dispatcher
from aiogram.types.message import Message, ParseMode
from aiogram.types import Chat

from aiogram.utils.markdown import escape_md

from config import CFG


async def handle_reload(message: Message):

    dispatcher = Dispatcher.get_current()

    user_login = dispatcher.middleware.applications[0]

    user_login.ready = False
    await user_login.prepare_models()

    await message.reply('初始化 UserLogin 完成')


def md_link(chat: Chat) -> str:
    title = escape_md(chat.title)
    user_name = escape_md(chat.username)
    
    return f'[{title} @{user_name}](https://t.me/{user_name})'


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
        parse_mode=ParseMode.MARKDOWN)
