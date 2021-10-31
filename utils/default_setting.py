'''
# @Author       : Chr_
# @Date         : 2021-10-27 23:22:58
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-31 14:17:19
# @Description  : 初始化数据库
'''

from typing import Tuple
from loguru import logger

from models.level import Levels
from models.right import Rights



async def get_default_setting() -> Tuple[Levels, Rights]:
    '''
    # @Description: 初始化数据库
    '''
    # 读取默认权限和等级

    default_level = await Levels.get_or_none(default=True)

    if not default_level:  # 不存在就创建
        default_level = await Levels.create(
            default=True,
            disp_name='Null',
            min_exp=-1,
            max_exp=-1,
        )
        logger.info('Create default level')
        

    default_right = await Rights.get_or_none(default=True)

    if not default_right:  # 不存在就创建
        default_right = await Rights.create(
            default=True,
            disp_name='默认权限',
            can_post=True,
            can_rating=True,
            can_review=False,
            can_auto_approval=False,
            can_one_vote=False,
            can_use_cmd=True,
            can_use_admin_cmd=False,
            can_use_super_cmd=False
        )
        logger.info('Create default right')

    return (default_level, default_right)