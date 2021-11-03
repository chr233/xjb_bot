'''
# @Author       : Chr_
# @Date         : 2021-10-29 18:12:45
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-03 14:00:22
# @Description  : 
'''

from aiogram.types import Message
from aiogram.types.message import ParseMode
import aiogram.utils.markdown as md
from models.badge import Badges
from models.level import Levels

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

    info = '\n'.join([
        f"昵称: `{nick}`",
        f"等级: `{level}`",
        f"权限: `{right}`",
        f"徽章: `{badges}`",
        "="*15,
        f'采用稿件: `{accept}`',
        f'被拒稿件: `{reject}`',
        f'投稿总数: `{post}`',
        f'审核总数: `{review}`',
        f'评价总数: `{rating}`',
        "="*15,
        f"经验: `{exp}`",
        '投稿、审核、评分都可以获得经验哦'
    ])

    await message.reply(info, parse_mode=ParseMode.MARKDOWN)
