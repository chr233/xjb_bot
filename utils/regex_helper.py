'''
# @Author       : Chr_
# @Date         : 2021-11-22 16:42:29
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-22 17:58:24
# @Description  : 正则表达式
'''

from re import compile
from typing import List, Tuple
from loguru import logger


HASH_TAG = compile(r'#\S+')
BLANKS = compile(r'\s+')


def pure_caption(text:str)->str:
    '''
    过滤一些tag
    '''
    txt = HASH_TAG.sub('',text)
    txt = BLANKS.sub(' ',txt)
    return txt.strip()