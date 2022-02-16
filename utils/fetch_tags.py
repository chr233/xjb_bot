'''
# @Author       : Chr_
# @Date         : 2022-02-16 14:21:15
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-16 21:10:47
# @Description  : 
'''

from re import compile
from models.tag import RegexpTags, NameLTags


def text_fatch_tagid(text: str) -> int:
    '''根据文本获取标签'''
    tagnum = 0

    for tagid, regexp in RegexpTags:
        if regexp.match(text):
            tagnum += tagid

    return tagnum


def tagid_fetch_text(tagnum: int) -> str:
    '''根据标签id获取文本'''
    tags = []

    for tagid,  name_l in NameLTags:
        if tagnum & tagid:
            tags.append(name_l)

    return ' '.join(tags)


GRUB_TAGID = compile(r'\s(\d+)$')


def str_fetch_tagid(text: str) -> int:
    '''文本提取数字tagid'''

    match = GRUB_TAGID.search(text)
    if not match:
        return 0
    else:
        return int(match.group(1))
