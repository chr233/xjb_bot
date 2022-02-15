'''
# @Author       : Chr_
# @Date         : 2021-11-03 19:46:39
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-12 17:17:29
# @Description  : 投稿按钮
'''

from aiogram.types.inline_keyboard import InlineKeyboardButton as IKButon, InlineKeyboardMarkup

from utils.emojis import GHOST, SMILE, NO, YES, WATER


class SubmitPostKey():
    anymouse_on = 'sp_anymouse_on'      # 匿名模式
    anymouse_off = 'sp_anymouse_off'    # 实名模式
    cancel = 'sp_cancel'                # 取消投稿
    post = 'sp_post'                    # 投稿
    post_anymouse = 'sp_post_anymouse'  # 投稿(匿名模式)


__submit_post_kbd_named = [
    [IKButon(f'{SMILE}保留来源', callback_data=SubmitPostKey.anymouse_on)],
    [IKButon(f'{NO}取消', callback_data=SubmitPostKey.cancel),
     IKButon(f'{YES}投稿', callback_data=SubmitPostKey.post)]
]

__submit_post_kbd_anymouse = [
    [IKButon(f'{GHOST}匿名投稿', callback_data=SubmitPostKey.anymouse_off)],
    [IKButon(f'{NO}取消', callback_data=SubmitPostKey.cancel),
     IKButon(f'{YES}投稿', callback_data=SubmitPostKey.post_anymouse)]
]


def gen_submit_keyboard(anymouse: bool = False) -> InlineKeyboardMarkup:
    kbd = __submit_post_kbd_anymouse if anymouse else __submit_post_kbd_named
    return InlineKeyboardMarkup(inline_keyboard=kbd)
