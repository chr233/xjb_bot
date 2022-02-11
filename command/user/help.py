'''
# @Author       : Chr_
# @Date         : 2021-10-29 18:12:45
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-12 00:59:21
# @Description  : 
'''

from turtle import Turtle
from typing import Tuple
from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types.message import Message, ParseMode
from loguru import logger
from .static import BOT_MSG, VER_MSG, CMD_HELP

from config import VERSION, BOT_NICK

__CMDs = {
    'USER': (
        ('start', '开始使用'),
        ('help', '查看帮助'),
        ('myinfo', '查看用户信息'),
    ),
    'ADMIN': (
        ('top', '查看服务器状态'),
    ),
    'SUPER': (
        ('reload', '重新加载配置文件'),
    ),
}


def generate_help(cmd: Tuple[Tuple[Tuple[str, str]]]) -> str:
    result = []
    for data in cmd:
        temp = []
        for (cmd,desc) in data:
            temp.append(f'/{cmd} \\- {desc}')            
            
        result.append('\n'.join(temp))
        
    return '\n\n'.join(result)

CMD_HELP = {
    'NULL': '无可奉告',
    'USER': generate_help((__CMDs['USER'],)),
    'ADMIN': generate_help((__CMDs['USER'],__CMDs['ADMIN'])),
    'SUPER': generate_help((__CMDs['USER'],__CMDs['ADMIN'],__CMDs['SUPER'])),
}

async def handle_help( message: Message):
    right = message.user.right

    if right.can_use_super_cmd:
        msg = CMD_HELP['SUPER']
    elif right .can_use_admin_cmd:
        msg = CMD_HELP['ADMIN']
    elif right.can_use_cmd:
        msg = CMD_HELP['USER']
    else:
        msg = CMD_HELP['NULL']

    await message.reply(msg, parse_mode=ParseMode.MARKDOWN_V2)
