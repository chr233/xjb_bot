'''
# @Author       : Chr_
# @Date         : 2021-10-27 22:29:09
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-03 16:01:07
# @Description  : 用户等级
'''

from tortoise.models import Model
from tortoise import fields

class Levels(Model):
    '''
    等级表
    '''
    
    id = fields.IntField(pk=True)
    
    default = fields.BooleanField(default=False) # 是否为默认
    
    disp_name = fields.CharField(max_length=20)

    min_exp = fields.IntField(default=-1) #自动升级的最低经验
    max_exp = fields.IntField(default=-1) #自动取消的最高经验
    
    reach_count = fields.IntField(default=0)  # 达成人数
 
    users:fields.ReverseRelation["Users"]
 
    class Mate:
        table = "levels"
        
    def __str__(self) -> str:
        return f'@{self.id} | {self.disp_name} | {self.reach_count}'
