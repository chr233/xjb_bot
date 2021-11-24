'''
# @Author       : Chr_
# @Date         : 2021-11-24 14:30:05
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-24 14:34:56
# @Description  : 生成Markdown链接
'''

from models.user import Users


def user_link(user: Users) -> str:
    return f'[{user.user_nick}](https://t.me/{user.user_name})'
