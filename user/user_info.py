'''
# @Author       : Chr_
# @Date         : 2021-10-29 18:12:45
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-31 14:27:59
# @Description  : 
'''

from aiogram.types import Message

async def getUserInfo(message: Message):
    user = message.from_user



async def myInfo(message: Message):
    user = message.user
        
    await message.reply(user.user_nick)