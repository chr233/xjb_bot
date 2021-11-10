'''
# @Author       : Chr_
# @Date         : 2021-11-10 14:16:00
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-10 14:32:53
# @Description  : 文字处理
'''

from .emojis import YES, NO


def bool2str(value: bool) -> str:
    '''
    将布尔值转换为字符串
    '''
    return YES if value else NO
