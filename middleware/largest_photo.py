'''
# @Author       : Chr_
# @Date         : 2021-11-03 15:13:24
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-03 15:57:35
# @Description  : 相同
'''


from typing import Dict
from loguru import logger
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

class LargestPhoto(BaseMiddleware):
    """
    为Message添加user属性
    """

    def __init__(self):
        logger.info('User login middleware loaded')
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        让Message对象带上当前用户
        """

        if not message.photo:
            return

        dic = {}

        for photo in message.photo:
            fid = photo.file_id
            od_photo = dic.get(fid, None)

            if not od_photo or photo.file_size > od_photo.file_size:
                dic[fid] = photo
        message.photo = list(dic.values())
        print(message)
