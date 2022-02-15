'''
# @Author       : Chr_
# @Date         : 2022-02-12 19:25:26
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-13 00:38:52
# @Description  : 处理
'''


from aiogram.types.message import Message

from buttons.submit import gen_submit_keyboard

from controller.permission import check_permission, Permissions

from .pre_post import pre_create_new_post


async def handle_text_message(message: Message):
    '''处理文字投稿'''
    # await message.reply('暂不支持文字投稿哟~')
    # raise CancelHandler()

    user = message.user
    anymouse_mode = user.prefer_anymouse

    if check_permission(user.right, Permissions.DirectPost):
        # 直接投稿
        ...
        keyboard = gen_submit_keyboard(anymouse_mode)
        resp = await message.reply('确定要投稿吗？\n\n可以选择是否保留来源', reply_markup=keyboard)

    else:
        keyboard = gen_submit_keyboard(anymouse_mode)
        resp = await message.reply('确定要投稿吗？\n\n可以选择是否保留来源', reply_markup=keyboard)

    await pre_create_new_post(message, resp, None)
