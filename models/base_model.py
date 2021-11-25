'''
# @Author       : Chr_
# @Date         : 2021-11-01 15:02:02
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-26 00:42:08
# @Description  : 基础数据类型
'''

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
    url: str = ''  # 链接名
    # 频道链接 https://t.me/{username}/{forward_from_nessage_id}
    # 用户链接 https://t.me/{username}
    # 另一种用户链接 tg://user?id={user_id}

    def __str__(self) -> str:
        return f'{self.name} {self.url}'
