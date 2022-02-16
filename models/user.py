'''
# @Author       : Chr_
# @Date         : 2021-10-27 16:52:43
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-17 00:06:24
# @Description  : 用户信息
'''

from html import escape
from urllib.parse import quote
from aiogram.utils.markdown import escape_md

from tortoise.models import Model
from tortoise import fields

from custom import custom_fields

# from .badge import Badges
# from .level import Levels
# from .right import Rights


class Users(Model):
    '''
    用户信息表
    '''

    id = fields.IntField(pk=True)

    user_id = fields.BigIntField(index=True, unique=True)  # 用户数字id
    user_nick = fields.CharField(max_length=255)  # 用户昵称
    user_name = fields.CharField(max_length=255)  # 用户@id

    is_ban = fields.BooleanField(default=False)  # 是否被封禁

    prefer_anymouse = fields.BooleanField(default=False)  # 是否默认开启匿名

    level: fields.ForeignKeyRelation["Levels"] = fields.ForeignKeyField(
        model_name="models.Levels", related_name="users",
        on_delete=fields.CASCADE
    )  # 用户等级
    right: fields.ForeignKeyRelation["Rights"] = fields.ForeignKeyField(
        model_name="models.Rights", related_name="users",
        on_delete=fields.CASCADE
    )  # 用户权限

    badges: fields.ManyToManyRelation["Badges"] = fields.ManyToManyField(
        model_name="models.Badges", related_name="users",
        through="users_badges", on_delete=fields.CASCADE
    )  # 用户所有徽章

    enable_badges = custom_fields.BadgesField(default="")  # 徽章列表

    accept_count = fields.IntField(default=0)  # 过审投稿数
    reject_count = fields.IntField(default=0)  # 被毙投稿数
    post_count = fields.IntField(default=0)    # 投稿总数
    review_count = fields.IntField(default=0)  # 审核总数

    exp_count = fields.IntField(default=0)     # 经验值
    # rating_count = fields.IntField(default=0)  # 评分数

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    posts: fields.ReverseRelation["Posts"]
    # ratings: fields.ReverseRelation["Ratings"]
    reviews_accept: fields.ReverseRelation["PublicPosts"]
    reviews_reject: fields.ReverseRelation["RejectPosts"]

    class Mate:
        table = "users"

    def __str__(self) -> str:
        return f'No.{self.id} | #{self.user_id} | {self.user_name} | {self.user_nick}'

    def tg_link(self) -> str:
        if self.user_name:
            return f'https://t.me/{self.user_name}'
        else:
            return f'tg://user?id={self.user_id}'

    def html_link(self) -> str:
        name = escape(self.user_nick)
        url = quote(self.tg_link())
        return f'<a href={url}>{name}</a>'

    def md_link(self) -> str:
        name = escape_md(self.user_nick)
        url = escape_md(self.tg_link())
        return f'[{name}]({url})'
