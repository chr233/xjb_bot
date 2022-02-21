'''
# @Author       : Chr_
# @Date         : 2021-11-01 09:46:32
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-21 15:07:55
# @Description  : 自定义orm字段
'''

import rapidjson
from pydantic import parse_obj_as
from typing import Iterable, List, Union
from tortoise.fields import TextField

from models.base_model import FileObj


class FileObjField(TextField):
    """
    使用TextField储存多个文件对象
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_db_value(self, value: Union[None, Iterable[FileObj]], instance) -> str:
        if not value:
            return ''
        else:
            files = [x.dict() for x in value]
            return rapidjson.dumps(files)
            # return msgpack.dumps(files)

    def to_python_value(self, value: Union[List[FileObj], str]) -> Union[None, List[FileObj]]:
        try:
            if not value:
                return []
            else:
                if isinstance(value, str):
                    raw = rapidjson.loads(value)
                    # raw = msgpack.loads(value)
                    data = parse_obj_as(List[FileObj], raw)
                elif isinstance(value, list) and isinstance(value[0], FileObj):
                    data = value
                else:
                    data = parse_obj_as(List[FileObj], value)
                return data
        except Exception:
            raise ValueError(
                f"Database value {value} can't unserialise to FileObj."
            )

class BadgesField(TextField):
    """
    使用TextField储存徽章ID
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_db_value(self, value: Union[None, List[int]], instance) -> str:
        if not value:
            return ''
        else:
            if isinstance(value, list) and isinstance(value[0], int):
                data = rapidjson.dumps(value)
                # data = msgpack.dumps(value)
            else:
                value = [x.id for x in value]
                data = rapidjson.dumps(value)
                # data = msgpack.dumps(value)

            return rapidjson.dumps(value)
            # return msgpack.dumps(value)

    def to_python_value(self, value: Union[str, List[int]]) -> Union[None, List[int]]:
        try:
            if not value:
                return None
            else:
                if isinstance(value, list):
                    data = value
                else:
                    data = rapidjson.loads(value)
                    # data = msgpack.loads(value)
                return data
        except Exception:
            raise ValueError(
                f"Database value {value} can't unserialise to badges_list."
            )
