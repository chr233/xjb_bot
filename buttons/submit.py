'''
# @Author       : Chr_
# @Date         : 2021-11-03 19:46:39
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-17 00:13:37
# @Description  : 投稿按钮
'''

from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton as IKButon

from utils.emojis import GHOST, SMILE, NO, YES


class SubmitPostKey():
    anymouse = 'sp_anymouse'  # 匿名模式
    cancel = 'sp_cancel'     # 取消投稿
    post = 'sp_post'         # 投稿


# 预制按钮
__submit_post_kbd_named = [
    [IKButon(f'{SMILE}保留来源', callback_data=SubmitPostKey.anymouse)],
    [IKButon(f'{NO}取消', callback_data=SubmitPostKey.cancel),
     IKButon(f'{YES}投稿', callback_data=SubmitPostKey.post)]
]

__submit_post_kbd_anymouse = [
    [IKButon(f'{GHOST}匿名投稿', callback_data=SubmitPostKey.anymouse)],
    [IKButon(f'{NO}取消', callback_data=SubmitPostKey.cancel),
     IKButon(f'{YES}投稿', callback_data=SubmitPostKey.post)]
]


def gen_submit_keyboard(anymouse: bool = False) -> InlineKeyboardMarkup:
    if anymouse:
        kbd = __submit_post_kbd_anymouse
    else:
        kbd = __submit_post_kbd_named
    return InlineKeyboardMarkup(inline_keyboard=kbd)
