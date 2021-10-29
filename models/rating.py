'''
# @Author       : Chr_
# @Date         : 2021-10-27 23:12:00
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-29 13:52:24
# @Description  : 
'''
from enum import IntEnum

from tortoise.models import Model
from tortoise import fields


class Rate_Choose(IntEnum):
    Default = 0
    LIKE = 1     # 喜欢
    CAO = 2      # 生草
    MARS = 3     # 火星
    DISLIKE = 4  # 不喜欢


class Ratings(Model):
    '''稿件评分模型'''
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField(
        model_name='models.Users', related_name='ratings')  # 评分用户

    post = fields.ForeignKeyField(
        model_name='models.Accepted_Posts', related_name='ratings')  # 评分稿件

    value = fields.IntEnumField(
        enum_type=Rate_Choose, default=Rate_Choose.Default)  # 评分值

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
