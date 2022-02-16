'''
# @Author       : Chr_
# @Date         : 2022-02-11 22:49:01
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-15 15:25:49
# @Description  : 版本信息命令
'''

from aiogram.utils.markdown import escape_md
from aiogram.types.message import Message, ParseMode
from .static import BOT_MSG, VER_MSG, BOT_NICK, VERSION

BOT_MSG = escape_md(f'{BOT_NICK} @ {VERSION}')

VER_MSG = escape_md(f'{BOT_NICK} Ver {VERSION} © 2022')


async def handle_start(message: Message):

    await message.reply(BOT_MSG, parse_mode=ParseMode.MARKDOWN)


async def handle_version(message: Message):

    await message.reply(VER_MSG, parse_mode=ParseMode.MARKDOWN)
