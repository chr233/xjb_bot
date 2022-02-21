'''
# @Author       : Chr_
# @Date         : 2021-11-03 19:46:43
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-18 00:05:46
# @Description  : 拒稿按钮
'''

from typing import List
from loguru import logger
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton as IKButon

from utils.emojis import NO, YES, CHECK, UNCHECK ,BACK

from models.reason import Reasons
from models.tag import NameSTags



class RejectPostKey():
    back = 'rj_back'      # 返回上级
    rejecj = 'rj_reject'  # 拒绝投稿
    custome = 'rj_custome'  # 自定义拒稿理由


class RejectKeyboardsHelper():
    ready = False

    __reasons: List[str] = None

    __buttons = [IKButon(f'{BACK}返回', callback_data=RejectPostKey.back)]

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
                        callback_data=f'{RejectPostKey.tag} {tagid}'))

        return btns


    async def gen_reject_keyboard(self, tagnum: int):
        '''获取拒稿键盘'''
        if not self.ready:
            await self.prepare_modules()

        kbd = [
            self.tagid_fetch_button(tagnum),
            self.__buttons
        ]

        return InlineKeyboardMarkup(inline_keyboard=kbd)


RJKH = RejectKeyboardsHelper()
