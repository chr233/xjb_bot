'''
# @Author       : Chr_
# @Date         : 2021-10-27 22:29:09
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-12 00:58:28
# @Description  : 用户权限组
'''

from tortoise.models import Model
from tortoise import fields

# from .user import Users


class Rights(Model):
    '''
    用户权限等级模型
    '''
    id = fields.IntField(pk=True)
    default = fields.BooleanField(default=False)  # 是否为默认

    disp_name = fields.CharField(max_length=20)  # 权限组名称

    can_post = fields.BooleanField(default=True)  # 是否可以投稿
    can_review = fields.BooleanField(default=False)  # 是否可以审稿
    can_direct_post = fields.BooleanField(default=False)  # 是否可以免审发布
    can_retract_post = fields.BooleanField(default=False)  # 是否可以撤回稿件

    can_use_cmd = fields.BooleanField(default=True)  # 是否可以使用一般命令
    can_use_admin_cmd = fields.BooleanField(default=False)  # 是否可以使用管理命令
    can_use_super_cmd = fields.BooleanField(default=False)  # 是否可以使用高级管理命令

    users: fields.ReverseRelation["Users"]

    class Mate:
        table = "rights"

    def __str__(self) -> str:
        return f'@{self.id} {self.disp_name}'
