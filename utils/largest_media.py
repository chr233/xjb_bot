'''
# @Author       : Chr_
# @Date         : 2021-11-24 12:16:11
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-24 14:14:10
# @Description  : 查找最大的媒体
'''

from typing import Iterable
from aiogram import types

from models.base_model import FileObj


def find_largest_media(media_obj: list = None) -> FileObj:
    '''
    获取最大的媒体对象
    '''

    if isinstance(media_obj, Iterable):
        max_size = 0
        largest = None

        for media in media_obj:
            if media.file_size > max_size:
                max_size = media.file_size
                largest = media
        if largest:
            return FileObj(
            file_id=largest.file_id,
            file_uid=largest.file_unique_id,
            file_size=largest.file_size,
            width=largest.width,
            height=largest.height,
        )
        else:
            return largest

    else:
        return None
