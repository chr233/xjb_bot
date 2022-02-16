'''
# @Author       : Chr_
# @Date         : 2021-10-28 15:45:44
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-16 21:52:37
# @Description  : 稿件标签
'''

from html import escape
import re

from typing import Dict, Pattern, Tuple
from tortoise.models import Model
from tortoise import fields

a = re.compile('')

__BUILDIN_TAGS = (
    (1, 'NSFW', '#NSFW', re.compile(r'NSFW', re.IGNORECASE)),
    (2, '朋友', '#我有一个朋友', re.compile(r'朋友|英雄')),
    (4, '晚安', '#晚安', re.compile(r'晚安')),
)

StaticTags = {
    tagid: (name_s, name_l) for tagid, name_s, name_l, _ in __BUILDIN_TAGS
}

RegexpTags = [
    (tagid, regexp) for tagid, _, _, regexp in __BUILDIN_TAGS
]

NameLTags = [
    (tagid,escape( name_l)) for tagid, _, name_l, _ in __BUILDIN_TAGS
]

NameSTags = [
    (tagid, name_s) for tagid, name_s, _, _ in __BUILDIN_TAGS
]

# class Tags(Model):
#     '''
#     标签模型
#     '''

#     id = fields.IntField(pk=True)
#     full_name = fields.CharField(max_length=50)  # 显示名称
#     short_name = fields.CharField(max_length=50)  # 短名称

#     class Mate:
#         table = "tags"
