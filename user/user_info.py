'''
# @Author       : Chr_
# @Date         : 2021-10-29 18:12:45
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-29 19:46:58
# @Description  : 
'''

from aiogram.types import Message

async def getUserInfo(message: Message):
    user = message.from_user



async def myInfo(message: Message):
    user = message.from_user
    
    user_nick = user.full_name
    user_name = user.mention
    user_id = user.id
    
    print(user)
    
    await message.reply(message.from_user.full_name)