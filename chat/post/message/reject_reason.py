'''
# @Author       : Chr_
# @Date         : 2022-02-17 09:21:53
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-17 09:37:40
# @Description  : 
'''

from aiogram.types.message import Message, ParseMode
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher import FSMContext

from buttons.submit import gen_submit_keyboard
from buttons.direct import DKH, DirectPostKey

from controller.permission import check_permission, Permissions

from .pre_post import pre_create_new_post


async def handle_custom_reject_reason(message: Message, state: FSMContext):
    '''处理文字投稿'''
    # await message.reply('暂不支持文字投稿哟~')
    # raise CancelHandler()

    user = message.user
    anymouse_mode = user.prefer_anymouse

    length = len(message.text)
    if length > 255:
        text = (
            '投稿内容过长, 请考虑分段发送\n'
            f'当前长度: `{length}` 字\n'
            '最大长度: `255` 字\n'
            '更多帮助: /help'
        )
        await message.reply(
            text=text,
            parse_mode=ParseMode.MARKDOWN
        )
        raise CancelHandler()

    if not check_permission(user.right, Permissions.DirectPost):
        # 确认后投稿
        keyboard = gen_submit_keyboard(anymouse_mode)
        text = '稿件审核后才会发布, 确定要投稿吗？\n\n可以选择是否保留来源'
        msg = await message.reply(text=text, reply_markup=keyboard)
        await pre_create_new_post(message, msg, None)