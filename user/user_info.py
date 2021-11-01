'''
# @Author       : Chr_
# @Date         : 2021-10-29 18:12:45
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-01 23:55:01
# @Description  : 
'''

from aiogram.types import Message
import aiogram.utils.markdown as md

from models.user import Users


async def myInfo(message: Message):
    user:Users = message.user
    
    level:Levels    
    
    info = (
        f"昵称: {user.user_nick}\n",
        f"等级: {user.user_nick}\n",
        f"徽章: {user.user_nick}\n",
        f": {user.user_nick}\n",
        f"用户名: {user.user_nick}\n",
        
        
    )
    
    await message.reply(user.user_nick)