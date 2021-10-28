'''
# @Author       : Chr_
# @Date         : 2021-10-27 22:29:09
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-28 15:53:40
# @Description  : 
'''

from tortoise.models import Model
from tortoise import fields


class Rights(Model):
    '''用户权限等级模型'''
    id = fields.IntField(pk=True)
    disp_name = fields.CharField(max_length=20)  # 权限名称

    can_post = fields.BooleanField(default=True)  # 是否可以投稿
    can_rating = fields.BooleanField(default=True)  # 是否可以评分
    can_review = fields.BooleanField(default=False)  # 是否可以审稿
    can_auto_approval = fields.BooleanField(default=False)  # 是否可以免审投稿
    can_one_vote = fields.BooleanField(default=False)  # 是否可以一票决定
    
    can_use_cmd = fields.BooleanField(default=True)  # 是否可以使用一般命令
    can_use_admin_cmd = fields.BooleanField(default=False)  # 是否可以使用管理命令
