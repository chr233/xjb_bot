'''
# @Author       : Chr_
# @Date         : 2021-10-28 15:45:44
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-31 13:15:46
# @Description  : 
'''

from tortoise.models import Model
from tortoise import fields


class Tags(Model):
    '''标签模型'''

    id = fields.IntField(pk=True)
    disp_name = fields.CharField(max_length=50)  # 显示名称
    real_name = fields.CharField(max_length=50)  # 实际名称
    is_wanan = fields.BooleanField(default=False)  # 是否为晚安投稿
    class Mate:
        table = "tags"
