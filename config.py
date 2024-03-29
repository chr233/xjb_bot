
'''
# @Author       : Chr_
# @Date         : 2021-03-13 19:34:20
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-16 12:29:21
# @Description  : 全局配置
'''

from enum import Enum
from typing import List, Union
from pydantic import BaseSettings as BS

VERSION = '1.0.0'

BOT_NICK = '心惊报投稿Bot'


class Bot_Modes(Enum):
    P: str = 'P'
    Polling: str = 'P'
    W: str = 'W'
    Webhook: str = 'W'


class Config(BS):
    DEBUG_MODE: bool = False

    DB_URL: str = 'sqlite://data.db'

    Generate_Schemas: bool = False

    PROXY: Union[str, None] = None

    Bot_Mode: Bot_Modes = Bot_Modes.P

    Bot_Token: str = ''

    Super_Admin: List[int] = []

    Review_Group: str = ''

    Accept_Channel: str = ''

    Reject_Channel: str = ''

    Wanan_Start: int = 0
    
    Wanan_End: int = 0
    
    Wanan_period: int = 0

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


CFG = Config()
