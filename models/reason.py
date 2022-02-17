'''
# @Author       : Chr_
# @Date         : 2021-10-28 18:26:12
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-17 17:27:12
# @Description  : 未过审原因模板
'''

from tortoise.models import Model
from tortoise import fields


StaticReason = (
    '不好笑',
    '发过了',
    '图糊了'
)

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
