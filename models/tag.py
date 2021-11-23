'''
# @Author       : Chr_
# @Date         : 2021-10-28 15:45:44
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-23 22:27:19
# @Description  : 稿件标签
'''

from typing import Dict, Tuple
from tortoise.models import Model
from tortoise import fields


StaticTags: Dict[int, Tuple[str]] = {
    1: ('NSFW', 'NSFW'),
    2: ('朋友', '我有一个朋友'),
    3: ('晚安', '晚安'),
}


class Tags(Model):
    '''
    标签模型
    '''

    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=50)  # 显示名称
    short_name = fields.CharField(max_length=50)  # 短名称

    class Mate:
        table = "tags"
