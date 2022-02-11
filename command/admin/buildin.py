'''
# @Author       : Chr_
# @Date         : 2022-02-11 18:30:44
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-11 19:41:11
# @Description  : 
'''

from loguru import logger

from aiogram.dispatcher import Dispatcher
from aiogram.types.message import Message

from models.right import Rights


BUILDIN_RIGHTS =(
    # 默认, 权限组名
    [1 ,'默认权限',1,1,0,0,0,0,0],
)


async def handle_add_buildin_rights(message: Message):
    '''生成内置权限组'''
    dispatcher = Dispatcher.get_current()

    normal = Rights.create(
        default=True,
                           disp_name='默认权限',
                           can_post=True,
                           can_rating=True,
                           can_review=False,
                           can_auto_approval=False,
                           can_one_vote=False,
                           can_use_cmd=True,
                           can_use_admin_cmd=False,
                           can_use_super_cmd=False)

    user_login.ready = False
    await user_login.prepare_models()

    await message.reply('初始化UserLogin完成')
