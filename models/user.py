'''
# @Author       : Chr_
# @Date         : 2021-10-27 16:52:43
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-29 19:22:05
# @Description  : 用户表
'''

from tortoise.models import Model
from tortoise import fields

class Users(Model):
    '''用户信息模型'''
    
    id = fields.IntField(pk=True)

    user_nick = fields.CharField(max_length=255)  # 用户昵称
    user_name = fields.CharField(max_length=255)  # 用户@id
    user_id = fields.CharField(max_length=255)  # 用户数字id

    level = fields.ForeignKeyField(
        model_name="models.Levels", related_name="users")  # 用户等级
    right = fields.ForeignKeyField(
        model_name="models.Rights", related_name="users")  # 用户权限
    badge = fields.ManyToManyField(
        model_name="models.Badges", related_name="users",through="users_badges")  # 用户权限

    accept_count = fields.IntField(default=0)  # 过审投稿数
    reject_count = fields.IntField(default=0)  # 被毙投稿数
    post_count = fields.IntField(default=0)  # 投稿总数

    exp_count = fields.IntField(default=0)  # 经验值
    rating_count = fields.IntField(default=0)  # 评分数

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
