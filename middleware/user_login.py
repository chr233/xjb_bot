'''
# @Author       : Chr_
# @Date         : 2021-10-30 21:41:44
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-02 00:00:28
# @Description  : 
'''
from aiogram.dispatcher.handler import CancelHandler
from loguru import logger

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from models.user import Users
from models.right import Rights
from models.level import Levels

from utils.default_setting import get_default_setting


class UserLogin(BaseMiddleware):
    """
    登陆
    """
    ready = False
    default_level: Levels = None
    default_right: Rights = None

    def __init__(self):
        logger.info('User login middleware loaded')
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        从数据库获取用户
        """

        if not self.ready:
            self.default_level, self.default_right = await get_default_setting()

        from_user = message.from_user

        uid = str(from_user.id)
        unick = from_user.full_name
        uname = from_user.mention

        user = await self.get_user(uid, unick, uname)

        if from_user.is_bot:
            logger.debug(f'阻止机器人用户 @{uname} {unick}')
            return CancelHandler()

        if user.is_ban:
            logger.debug(f'阻止被Ban用户 {user}')
            raise CancelHandler()

        right = await user.right.get()

        message.user = user
        message.right = right

    async def get_user(self, user_id: str, user_nick: str, user_name: str):
        user = await Users.get_or_none(user_id=user_id)

        if not user:
            user = await Users.create(
                user_id=user_id,
                user_name=user_name,
                user_nick=user_nick,
                right=self.default_right,
                level=self.default_level
            )

            self.default_level.reach_count += 1
            await self.default_level.save()

            logger.debug(f'创建新用户 {user}')

        if (user.user_nick != user_nick) or (user.user_id != user_id):
            user.user_nick = user_nick
            user.user_id = user_id
            await user.save()
            logger.debug(f'更新用户 {user}')

        return user
