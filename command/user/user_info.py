'''
# @Author       : Chr_
# @Date         : 2021-10-29 18:12:45
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-24 16:17:03
# @Description  : 用户信息
'''

from aiogram.types import Message
from aiogram.types.message import ParseMode

from models.user import Users


async def handle_myinfo(message: Message):
    user: Users = message.user
    nick = user.user_nick
    level = user.level.disp_name
    right = user.right.disp_name
    if user.enable_badges:
        badges = ','.join([x.disp_name for x in user.enable_badges])
    else:
        badges = '无'

    accept = user.accept_count
    reject = user.reject_count
    post = user.post_count
    rating = user.rating_count
    review = user.review_count
    exp = user.exp_count

    info = (
        f"昵称: `{nick}`\n"
        f"等级: `{level}`\n"
        f"权限: `{right}`\n"
        f"徽章: `{badges}`\n"
        "===============\n"
        f'采用稿件: `{accept}`\n'
        f'被拒稿件: `{reject}`\n'
        f'投稿总数: `{post}`\n'
        f'审核总数: `{review}`\n'
        f'评价总数: `{rating}`\n'
        "===============\n"
        f"经验: `{exp}`\n"
        '投稿、审核、评分都可以获得经验哦'
    )

    await message.reply(info, parse_mode=ParseMode.MARKDOWN_V2)
