'''
# @Author       : Chr_
# @Date         : 2021-11-03 15:13:24
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-24 00:54:21
# @Description  : 自动选择最大的图片
'''


from loguru import logger
from aiogram.types import Message
from aiogram.dispatcher.middlewares import BaseMiddleware


class LargestPhoto(BaseMiddleware):
    """
    删除Message对象中多余的photo
    """

    def __init__(self):
        logger.info('Largest photo middleware loaded')
        super().__init__()

    async def on_process_message(self, message: Message, data: dict):
        """
        让Message对象带上最大的图片
        """

        if not message.photo:
            return

        photos = message.photo
        largest = photos[0]

        if len(photos) > 1:
            for i in range(1, len(photos)):
                if photos[i].file_size > largest.file_size:
                    largest = photos[i]

        message.largest_photo = largest
