'''
# @Author       : Chr_
# @Date         : 2021-10-29 18:12:45
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-02 11:05:11
# @Description  : 
'''

from aiogram.types import Message
import aiogram.utils.markdown as md
from models.badge import Badges
from models.level import Levels

from models.user import Users


async def handle_info(message: Message):
    user: Users = message.user
    level = user.level
    badges = user.enable_badges
    

    info = (
        f"昵称: {user.user_nick}\n",
        f"等级: {user.user_nick}\n",
        f"徽章: {user.user_nick}\n",
        f": {user.user_nick}\n",
        f"用户名: {user.user_nick}\n",


    )

    await message.reply(user.user_nick)
