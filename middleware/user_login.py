'''
# @Author       : Chr_
# @Date         : 2021-10-30 21:41:44
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-16 12:55:07
# @Description  : 用户登录中间件
'''

from typing import Dict
from loguru import logger
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

from models.user import Users
from models.right import Rights
from models.level import Levels
from models.badge import Badges

from utils.default_setting import get_default_setting


class UserLogin(BaseMiddleware):
    """
    登录
    """
    ready = False
    __default_level: Levels = None
    __default_right: Rights = None
    __levels: Dict[int, Levels] = None
    __rights: Dict[int, Rights] = None
    __badges: Dict[int, Levels] = None

    def __init__(self):
        logger.info('User login middleware loaded')
        super().__init__()

    async def prepare_models(self):
        '''
        初始化模型
        '''
        self.__default_level, self.__default_right = await get_default_setting()
        levels = await Levels.all()
        rights = await Rights.all()
        badges = await Badges.all()

        self.__levels = {x.id: x for x in levels}
        self.__rights = {x.id: x for x in rights}
        self.__badges = {x.id: x for x in badges}

        logger.debug('初始化UserLogin完成')

        self.ready = True

    async def on_process_message(self, message: types.Message, data: dict):
        """
        让Message对象带上当前用户
        """

        if not self.ready:
            await self.prepare_models()

        from_user = message.from_user

        uid = str(from_user.id)
        unick = from_user.full_name
        uname = from_user.mention

        if not uname.startswith('@'):
            uname = ''

        if from_user.is_bot:
            logger.debug(f'阻止机器人用户 #{uid} | {uname} | {unick}')
            return CancelHandler()

        user = await self.get_user(uid, unick, uname)

        if user.is_ban:
            logger.debug(f'阻止被Ban用户 {user}')
            await message.reply('您已被限制访问')
            raise CancelHandler()

        message.user = user

    async def on_process_callback_query(self,  callback_query: types.CallbackQuery, data: dict):
        """
        让Callback_query对象带上当前用户
        """

        if not self.ready:
            await self.prepare_models()

        from_user = callback_query.from_user

        uid = str(from_user.id)
        unick = from_user.full_name
        uname = from_user.mention

        if from_user.is_bot:
            logger.debug(f'阻止机器人用户 #{uid} | {uname} | {unick}')
            return CancelHandler()

        user = await self.get_user(uid, unick, uname)

        if user.is_ban:
            logger.debug(f'阻止被Ban用户 {user}')
            # await callback_query.answer('无权访问', show_alert=True)
            raise CancelHandler()

        callback_query.user = user

    async def get_user(self, user_id: str, user_nick: str, user_name: str):
        '''
        读取用户信息
        '''
        user = await Users.get_or_none(user_id=user_id)

        if not user:
            user = await Users.create(
                user_id=user_id,
                user_name=user_name,
                user_nick=user_nick,
                right=self.__default_right,
                level=self.__default_level
            )

            self.__default_level.reach_count += 1
            await self.__default_level.save()

            logger.debug(f'创建新用户 {user}')

        if (user.user_nick != user_nick or user.user_name != user_name):
            user.user_nick = user_nick
            user.user_name = user_name
            await user.save()
            logger.debug(f'更新用户 {user}')

        if not user.is_ban:
            user.right = self.__rights.get(user.right_id, self.__default_right)
            user.level = self.__levels.get(user.level_id, self.__default_level)
            if user.enable_badges:
                badges = [
                    self.__badges[x]
                    for x in user.enable_badges
                    if x in self.__badges
                ]
                user.enable_badges = badges

        return user
