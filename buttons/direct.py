'''
# @Author       : Chr_
# @Date         : 2022-02-12 17:04:22
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-17 01:47:23
# @Description  : 直发投稿
'''

from typing import List
from loguru import logger
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton as IKButon

from utils.emojis import GHOST, NO, SMILE, YES, CHECK, UNCHECK


from models.tag import NameSTags


class DirectPostKey():
    anymouse = 'dp_anymouse'      # 匿名模式
    cancel = 'dp_cancel'                # 取消投稿
    post = 'dp_post'                    # 发布
    tag = 'dp_tag'                   # 标签


class DirectKeyboardsHelper():
    
    
    __buttons = [IKButon(f'{NO}取消', callback_data=DirectPostKey.cancel),
                IKButon(f'{YES}发布', callback_data=DirectPostKey.post)]

    __named = [IKButon(f'{SMILE}保留来源', callback_data=DirectPostKey.anymouse)]
    __anymouse = [IKButon(f'{GHOST}匿名投稿', callback_data=DirectPostKey.anymouse)]



    def __init__(self) -> None:
        ...

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
                        callback_data=f'{DirectPostKey.tag} {tagid}'))

        return btns

    def gen_direct_keyboard(self, tagnum: int, anymouse: bool = False):
        '''获取审核键盘'''

        kbd = [
                self.tagid_fetch_button(tagnum),
                self.__anymouse if anymouse else self.__named,
                self.__buttons
            ]

        return InlineKeyboardMarkup(inline_keyboard=kbd)


DKH = DirectKeyboardsHelper()
