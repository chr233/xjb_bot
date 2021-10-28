'''
# @Author       : Chr_
# @Date         : 2021-10-27 22:29:09
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-28 12:38:21
# @Description  : 
'''

from tortoise.models import Model
from tortoise import fields


class Levels(Model):
    id = fields.IntField(pk=True)
    disp_name = fields.CharField(max_length=20)

    min_exp = fields.IntField(default=-1)
    max_exp = fields.IntField(default=-1)
    

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
