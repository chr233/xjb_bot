'''
# @Author       : Chr_
# @Date         : 2021-10-29 18:12:45
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-02 14:13:52
# @Description  : 
'''

from aiogram.types.message import Message, ParseMode
from .static import BOT_MSG, VER_MSG, CMD_HELP


async def handle_start(message: Message):

    await message.reply(BOT_MSG, parse_mode=ParseMode.MARKDOWN_V2)


async def handle_help(message: Message):
    right = message.user.right

    if right.can_use_super_cmd:
        msg = CMD_HELP['SUPER']
    elif right .can_use_admin_cmd:
        msg = CMD_HELP['ADMIN']
    elif right.can_use_cmd:
        msg = CMD_HELP['NORMAL']
    else:
        msg = CMD_HELP['NULL'] 

    await message.reply(msg, parse_mode=ParseMode.MARKDOWN_V2)


async def handle_version(message: Message):

    await message.reply(VER_MSG, parse_mode=ParseMode.MARKDOWN_V2)
