'''
# @Author       : Chr_
# @Date         : 2022-02-12 17:04:22
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-16 14:19:44
# @Description  : 直发投稿
'''

from typing import Dict, List, Tuple
from aiogram.types.inline_keyboard import InlineKeyboardButton as IKButon, InlineKeyboardMarkup
from loguru import logger

from utils.emojis import GHOST, SMILE, NO, YES, WATER, CHECK, UNCHECK

from models.tag import StaticTags
from models.reason import Reasons


class DirectPostKey():
    anymouse_on = 'dp_anymouse'      # 匿名模式
    cancel = 'dp_cancel'                # 取消投稿
    post = 'dp_post'                    # 发布
    tag = 'dp_tag'  # 标签


class DirectKeyboardsHelper():
    ready = False

    __tags_short: List[Tuple[int, str]] = None
    __tags_full: List[Tuple[int, str]] = None

    __buttons: List[Tuple[str, str]] = None

    def __init__(self) -> None:
        ...

    async def get_tag(self, selected: int) -> str:
        if not self.ready:
            await self.prepare_modules()

        if not selected or selected == 0:
            return ''

        tags = [
            f'#{name}' for id, name in self.__tags_full if selected & id
        ]

        return ' '.join(tags)

    async def prepare_modules(self):
        self.__tags_short = [(x, y[0]) for x, y in StaticTags.items()]
        self.__tags_full = [(x, y[1]) for x, y in StaticTags.items()]

        self.__buttons = [
            (f'{NO}拒绝', DirectPostKey.reject), (f'{YES}采用', DirectPostKey.accept)
        ]

        logger.debug('初始化ReviewKeyboardsHelper完成')

        self.ready = True

    async def get_tag_keyboard_short(self, selected: int):
        if not self.ready:
            await self.prepare_modules()

        kbd = [
            [IKButon((CHECK if selected & id else UNCHECK) + name,
                     callback_data=f'{DirectPostKey.tag} {selected ^ id}')
                for id, name in self.__tags_short],
            [IKButon(text, callback_data=f'{data} {selected}')
                for text, data in self.__buttons]
        ]

        return InlineKeyboardMarkup(inline_keyboard=kbd)

    async def get_tag_keyboard_full(self, selected: int):
        if not self.ready:
            await self.prepare_modules()

        kbd = [
            [IKButon((CHECK if selected & id else UNCHECK) + name,
                     callback_data=f'{DirectPostKey.tag} {selected ^ id}')
                for id, name in self.__tags_full],
            [IKButon(text, callback_data=f'{data} {selected}')
                for text, data in self.__buttons]
        ]

        return InlineKeyboardMarkup(inline_keyboard=kbd)


DKH = DirectKeyboardsHelper()
