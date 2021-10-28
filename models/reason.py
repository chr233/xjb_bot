'''
# @Author       : Chr_
# @Date         : 2021-10-28 18:26:12
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-28 18:32:57
# @Description  : 
'''

from tortoise.models import Model
from tortoise import fields


class Reasons(Model):
    '''未过审原因模板'''
    id = fields.IntField(pk=True)
    template = fields.CharField(max_length=255)  # 拒绝原因模板

