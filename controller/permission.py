'''
# @Author       : Chr_
# @Date         : 2021-10-31 15:20:26
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-10 23:53:35
# @Description  : 权限控制
'''

from enum import IntEnum
from functools import wraps
from typing import Union
from aiogram import types
from loguru import logger

from models.right import Rights


class Permissions(IntEnum):
    '''
    权限类型
    '''
    Null = 0
    Post = 1
    Rating = 2
    Review = 3
    AutoApproval = 4
    OneVote = 5
    Cmd = 10
    AdminCmd = 20
    SuperCmd = 30


def check_permission(right: Rights, permission: Permissions):
    '''
    检查是否有对应的权限
    '''
    if permission == Permissions.Null:
        return True
    elif permission == Permissions.Post:
        return right.can_post
    elif permission == Permissions.Rating:
        return right.can_rating
    elif permission == Permissions.Review:
        return right.can_review
    elif permission == Permissions.AutoApproval:
        return right.can_auto_approval
    elif permission == Permissions.OneVote:
        return right.can_one_vote
    elif permission == Permissions.Cmd:
        return right.can_use_cmd
    elif permission == Permissions.AdminCmd:
        return right.can_use_admin_cmd
    elif permission == Permissions.SuperCmd:
        return right.can_use_super_cmd
    else:
        return False


def need_permission(permission: Permissions):
    '''
    权限检查装饰器
    '''

    def decorator(callback):
        @wraps(callback)
        async def wrapper(paylaod: Union[types.Message, types.CallbackQuery]):

            if check_permission(paylaod.user.right, permission):
                await callback(paylaod)
            else:
                logger.debug(f'鉴权失败 {paylaod.user}')
                await paylaod.reply('没有权限')

        return wrapper

    return decorator
