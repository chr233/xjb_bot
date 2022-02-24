'''
# @Author       : Chr_
# @Date         : 2021-11-03 19:46:43
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-22 18:59:54
# @Description  : 拒稿按钮
'''

from re import compile
from typing import Dict, List
from loguru import logger
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton as IKButon

from utils.emojis import CHAT, GHOST, NO, YES, CHECK, UNCHECK, BACK, PIN

from models.reason import Reasons, StaticReason
from models.tag import NameSTags


class RejectPostKey():
    back = 'rj_back'      # 返回上级
    rejecj = 'rj_reject'  # 拒绝投稿
    slience = 'rj_slience'  # 自定义拒稿理由


GRUB_REASONID = compile(r' @?(\d+)$')


class RejectKeyboardsHelper():
    ready = False

    __reasons: Dict[str, str] = {}

    __buttons = [IKButon(f'{BACK} 返回', callback_data=RejectPostKey.back),
                 IKButon(f'{GHOST} 静默拒稿', callback_data=RejectPostKey.slience)]

    __static_reason = [IKButon(f'{PIN} {s}', callback_data=f'{RejectPostKey.rejecj} @{i}')
                       for i, s in enumerate(StaticReason, 1)]

    __dynamic_reasons: List[IKButon] = None

    def __init__(self) -> None:
        ...

    async def prepare_modules(self):
        '''初始化模块'''

        db_reasons = await Reasons.all().limit(3).order_by('-id')

        self.__dynamic_reasons = [IKButon(f'{CHAT} {r.reason}', callback_data=f'{RejectPostKey.rejecj} {r.id}')
                                  for r in db_reasons]

        reasons = {}

        for i, s in enumerate(StaticReason, 1):
            reasons[str(i)] = s

        for r in db_reasons:
            reasons[f'@{r.id}'] = r.reason

        self.__reasons = reasons

        logger.debug('初始化 RejectKeyboardsHelper 完成')

        self.ready = True

    async def gen_reject_keyboard(self):
        '''获取拒稿键盘'''
        if not self.ready:
            await self.prepare_modules()

        reasons = self.__dynamic_reasons

        if len(reasons) > 1:
            kbd = [
                self.__buttons,
                *self.__static_reason,
                *reasons
            ]
        else:
            kbd = [
                self.__buttons,
                *self.__static_reason,
            ]

        return InlineKeyboardMarkup(inline_keyboard=kbd)

    async def str_fetch_reason(self, text: str) -> str:
        '''回调信息获取具体原因'''
        # 带@的是静态原因, 不带的是动态原因
        
        match = GRUB_REASONID.search(text)
        if not match:
            return None
        else:
            rid = match.group(1)
            reason = self.__reasons.get(rid)
            if reason:
                return reason
            else:
                # 未匹配到具体原因
                if not rid.startswith('@'):
                    # 从数据库中查找
                    rea = await Reasons.get_or_none(id=rid)
                    if rea:
                        return rea.reason
                    else:
                        return None
                else:
                    return None


RJKH = RejectKeyboardsHelper()
