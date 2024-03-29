'''
# @Author       : Chr_
# @Date         : 2021-10-27 23:12:00
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-11 18:33:10
# @Description  : 用户评分【弃用】
'''
from enum import IntEnum

from tortoise.models import Model
from tortoise import fields


class RatingValue(IntEnum):
    '''
    评分类型
    '''

    Default = 0
    LIKE = 1     # 喜欢
    CAO = 2      # 生草
    DISLIKE = 3  # 不喜欢
    MARS = 4     # 火星

    def __str__(self) -> str:
        return self.name


# 弃用
class Ratings(Model):
    '''稿件评分模型'''
    id = fields.IntField(pk=True)

    post: fields.ForeignKeyRelation["PublicPosts"] = fields.ForeignKeyField(
        model_name='models.PublicPosts', related_name='ratings'
    )  # 评分对象

    user: fields.ForeignKeyRelation["Users"] = fields.ForeignKeyField(
        model_name='models.Users', related_name='ratings'
    )  # 评分用户

    value = fields.IntEnumField(
        enum_type=RatingValue, default=RatingValue.Default
    )  # 评分值

    modified_at = fields.DatetimeField(auto_now=True)

    class Mate:
        table = "ratings"
        indexes = (
            ("post", "user"),
        )
        unique_together = (
            ("post", "user"),
        )

    def __str__(self):
        return f'@{self.id} {self.value}'
