'''
# @Author       : Chr_
# @Date         : 2021-11-01 09:46:32
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-01 23:21:39
# @Description  : 
'''

import rapidjson
from pydantic import parse_obj_as
from typing import Iterable, List, Union
from tortoise.fields import TextField

from models.base_model import FileObj, SourceLink


class FileObjField(TextField):
    """
    An example extension to CharField that serializes Enums
    to and from a str representation in the DB.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_db_value(self, value: Union[None, Iterable[FileObj]], instance) -> str:
        if not value:
            return ''
        else:
            files = [x.dict() for x in value]
            return rapidjson.dumps(files)

    def to_python_value(self, value: str) -> Union[None, List[FileObj]]:
        try:
            if not value:
                return []
            else:
                if isinstance(value, str):
                    raw = rapidjson.loads(value)
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


class LinkObjField(TextField):
    """
    An example extension to CharField that serializes Enums
    to and from a str representation in the DB.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_db_value(self, value: Union[None, SourceLink], instance) -> str:
        if not value:
            return ''
        else:
            return rapidjson.dumps(value.dict())

    def to_python_value(self, value: Union[str, SourceLink]) -> Union[None, SourceLink]:
        try:
            if not value:
                return None
            else:
                if isinstance(value, str):
                    data = SourceLink.parse_raw(value)
                elif isinstance(value, SourceLink):
                    data = value
                else:
                    data = SourceLink.parse_obj(value)
                return data
        except Exception:
            raise ValueError(
                f"Database value {value} can't unserialise to SourceLink."
            )
