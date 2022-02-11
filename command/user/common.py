'''
# @Author       : Chr_
# @Date         : 2022-02-11 22:49:01
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-12 02:09:37
# @Description  : 通用命令
'''

from aiogram.types.message import Message, ParseMode
from .static import BOT_MSG, VER_MSG, BOT_NICK, VERSION

BOT_MSG = f'{BOT_NICK} @ {VERSION}'

VER_MSG = f'*{BOT_NICK}* Ver `{VERSION}` © 2022'


async def handle_start(message: Message):

    await message.reply(BOT_MSG, parse_mode=ParseMode.MARKDOWN_V2)


async def handle_version(message: Message):

    await message.reply(VER_MSG, parse_mode=ParseMode.MARKDOWN_V2)
