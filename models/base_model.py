'''
# @Author       : Chr_
# @Date         : 2021-11-01 15:02:02
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-21 14:38:56
# @Description  : 基础数据类型
'''

from html import escape
from urllib.parse import quote
from aiogram.utils.markdown import escape_md, quote_html

from pydantic import BaseModel


class FileObj(BaseModel):
    '''
    单个文件对象
    '''
    file_id: str = ''
    file_uid: str = ''
    file_size: str = 0
    file_type: str = 'photo'
    # width: int = 0
    # height: int = 0

    def __str__(self) -> str:
        return self.file_uid


class SourceLink(BaseModel):
    '''
    消息链接
    '''
    name: str = ''  # 显示名称
    id: str = ''    # 对象ID (以@开头代表频道,数字代表用户)

    # 频道链接 https://t.me/{user_name}/{forward_from_nessage_id}
    # 另一种用户链接 tg://user?id={user_id}

    def __str__(self) -> str:
        name = self.name
        id = self.id

        if id.startswith('@'):
            return f'{name} https://t.me/{id}'
        else:
            return f'{name} tg://user?id={id}'

    def html_link(self) -> str:
        name = self.name
        id = self.id

        if id.startswith('@'):
            url = f'https://t.me/{id}'
        else:
            url = f'tg://user?id={id}'

        return quote_html(f'<a href={url}>{name}</a>')

    def md_link(self) -> str:
        name = escape_md(self.name)
        id = escape_md(self.id)

        if id.startswith('@'):
            url = f'https://t.me/{id}'
        else:
            url = f'tg://user?id={id}'

        return f'[{name}]({url})'
