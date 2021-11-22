'''
# @Author       : Chr_
# @Date         : 2021-11-03 19:46:43
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-23 00:29:38
# @Description  : 审核按钮
'''
from aiogram.types.inline_keyboard import InlineKeyboardButton as IKButon, InlineKeyboardMarkup

from utils.emojis import GHOST, SMILE, NO, YES, WATER


class ReviewPostKey():
    accept = 'sp_post'           # 接受投稿
    reject = 'sp_post_anymouse'  # 拒绝投稿


__review_post_kbd = [
    [IKButon(f'{NO}拒绝', callback_data=ReviewPostKey.reject)],
    [IKButon(f'{YES}采用 #NSFW', callback_data=ReviewPostKey.accept)],
    [IKButon(f'{YES}采用', callback_data=ReviewPostKey.accept)],
]

__review_post_kbd_accept_tag = [
    [IKButon(f'{GHOST}匿名投稿', callback_data=ReviewPostKey.anymouse_off)],
    [IKButon(f'{NO}取消', callback_data=ReviewPostKey.reject),
     IKButon(f'{YES}投稿', callback_data=ReviewPostKey.reject)]
]


def gen_review_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=__review_post_kbd)

def 