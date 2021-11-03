'''
# @Author       : Chr_
# @Date         : 2021-10-28 12:17:58
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-03 15:57:54
# @Description  : 用户徽章
'''

from tortoise.models import Model
from tortoise import fields


class Badges(Model):
    '''
    徽章表
    '''
    id = fields.IntField(pk=True)

    disp_name = fields.CharField(max_length=20)  # 显示名称

    can_apply = fields.BooleanField(default=False)  # 能否自助申请

    min_approve = fields.IntField(default=-1)  # 过审稿件数量
    min_experience = fields.IntField(default=-1)  # 经验
    min_vote = fields.IntField(default=-1)  # 投票数量

    reach_count = fields.IntField(default=0)  # 达成人数

    users: fields.ManyToManyRelation["Users"]

    modified_at = fields.DatetimeField(auto_now=True)

    class Mate:
        table = "badges"

    def __str__(self) -> str:
        return f'@{self.id} | {self.disp_name} | {self.reach_count}'
