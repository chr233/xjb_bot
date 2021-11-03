'''
# @Author       : Chr_
# @Date         : 2021-10-28 18:26:12
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-03 15:59:58
# @Description  : 未过审原因模板
'''

from tortoise.models import Model
from tortoise import fields


class Reasons(Model):
    '''
    未过审原因模板
    '''
    id = fields.IntField(pk=True)
    reason = fields.CharField(max_length=255)  # 拒绝原因模板

    class Mate:
        table = "reasons"
        
    def __str__(self):
        return f'@{self.id} {self.template}'
