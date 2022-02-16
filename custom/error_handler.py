'''
# @Author       : Chr_
# @Date         : 2021-11-22 23:28:42
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-16 18:51:58
# @Description  : 错误处理
'''

from aiogram.utils.exceptions import MessageNotModified
from aiogram.types.update import Update
from loguru import logger


async def error_handler(payload: Update, error: Exception):
    '''错误处理器'''

    logger.error(payload)
    logger.error(error)

    if isinstance(error, MessageNotModified):
        logger.debug(f'MessageNotModified: {error}')

    else:
        raise error
