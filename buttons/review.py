'''
# @Author       : Chr_
# @Date         : 2021-11-03 19:46:43
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-17 01:48:35
# @Description  : 审核按钮
'''

from typing import List
from loguru import logger
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton as IKButon

from utils.emojis import NO, YES, CHECK, UNCHECK

from models.reason import Reasons
from models.tag import NameSTags


class ReviewPostKey():
    accept = 'rp_accept'  # 接受投稿
    reject = 'rp_reject'  # 拒绝投稿
    tag = 'rp_tag'  # 标签


class ReviewKeyboardsHelper():
    ready = False

    __reasons: List[str] = None

    __buttons = [IKButon(f'{NO}拒绝', callback_data=ReviewPostKey.reject),
                 IKButon(f'{YES}采用', callback_data=ReviewPostKey.accept)]

    def __init__(self) -> None:
        ...

    async def prepare_modules(self):
        '''初始化模块'''
        reasons = await Reasons.all()
        self.__reasons = [reason.reason for reason in reasons]

        logger.debug('初始化ReviewKeyboardsHelper完成')

        self.ready = True

    @staticmethod
    def tagid_fetch_button(tagnum: int) -> List[IKButon]:
        '''根据标签id生成按钮'''
        btns = []

        for tagid, name_s in NameSTags:
            if tagnum & tagid:
                ico = CHECK
            else:
                ico = UNCHECK

            btns.append(IKButon(f'{ico}{name_s}',
                        callback_data=f'{ReviewPostKey.tag} {tagid}'))

        return btns

    async def gen_review_keyboard(self, tagnum: int):
        '''获取审核键盘'''
        if not self.ready:
            await self.prepare_modules()

        kbd = [
            self.tagid_fetch_button(tagnum),
            self.__buttons
        ]

        return InlineKeyboardMarkup(inline_keyboard=kbd)

    async def gen_reject_keyboard(self, tagnum: int):
        '''获取拒稿键盘'''
        if not self.ready:
            await self.prepare_modules()

        kbd = [
            self.tagid_fetch_button(tagnum),
            self.__buttons
        ]

        return InlineKeyboardMarkup(inline_keyboard=kbd)


RKH = ReviewKeyboardsHelper()
