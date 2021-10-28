
'''
# @Author       : Chr_
# @Date         : 2021-03-13 19:34:20
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-28 17:14:26
# @Description  : 全局配置
'''

from typing import List
from pydantic import BaseSettings as BS

VERSION = '1.0.0'


class Config(BS):
    DEBUG_MODE: bool = False

    DB_URL: str = 'sqlite://data.db'

    PROXY: str = None

    Bot_Token: str = ''

    Super_Admin: List[int] = []

    Review_Channel: str = ''

    Accept_Channel: str = ''

    Reject_Channel: str = ''

    Wanan_Start: int = 0
    Wanan_End: int = 0
    Wanan_period: int = 0

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


CFG = Config()
