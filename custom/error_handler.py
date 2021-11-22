'''
# @Author       : Chr_
# @Date         : 2021-11-22 23:28:42
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-22 23:41:55
# @Description  : 错误处理
'''

from aiogram.types.update import Update
from loguru import logger


async def error_handler(payload: Update, error: Exception):
    logger.error(payload)
    logger.error(error)
