'''
# @Author       : Chr_
# @Date         : 2021-10-27 23:22:58
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-21 19:14:11
# @Description  : 初始化数据库
'''

from typing import Tuple
from loguru import logger

from models.level import Levels
from models.right import Rights


__BUILDIN_RIGHTS = (
    # 第一个为默认
    # 显示名       post review direct retract cmd admin super
    ('用户',       1, 1, 0, 0,                1, 0, 0),
    ('审核员',     1, 1, 1, 0,                1, 0, 0),
    ('管理员',     1, 1, 1, 1,                1, 1, 0),
    ('超级管理员', 1, 1, 1, 1,                1, 1, 1),
    ('封禁用户',   0, 0, 0, 0,                0, 0, 0),
)

__BUILDIN_LEVEL = (
    # 第一个为默认
    # 显示名  min_exp max_exp
    ('Lv 0', 0,      10),
    ('Lv 1', 11,     100),
    ('Lv 2', 101,    200),
    ('Lv 3', 201,    500),
    ('Lv 4', 501,    1000),
    ('Lv 5', 1001,   5000),
    ('Lv 6', 5001,   -1),
    ('Lv -', -1,     -1),
)


async def get_default_setting() -> Tuple[Levels, Rights]:
    '''
    # @Description: 初始化数据库
    '''
    # 读取默认权限和等级

    default_level = await Levels.filter(default=True).limit(1)

    if not default_level:  # 不存在就创建
        levels = []
        for (name, a, b) in __BUILDIN_LEVEL:
            level = await Levels.create(
                default=False,
                disp_name=name,
                min_exp=a,
                max_exp=b
            )
            levels.append(level)

        default_level = levels[0]
        default_level.default = True
        await default_level.save()

        logger.info(f'创建 {len(levels)} 个等级')
    else:
        default_level = default_level[0]

    default_right = await Rights.filter(default=True).limit(1)

    if not default_right:  # 不存在就创建
        rights = []
        for (name, a, b, c, d, e, f, g) in __BUILDIN_RIGHTS:
            right = await Rights.create(
                default=False,
                disp_name=name,
                can_post=a,
                can_review=b,
                can_direct_post=c,
                can_retract_post=d,
                can_use_cmd=e,
                can_use_admin_cmd=f,
                can_use_super_cmd=g,
            )
            rights.append(right)

        default_right = rights[0]
        default_right.default = True
        await default_right.save()

        logger.info(f'创建 {len(rights)} 个权限组')
    else:
        default_right = default_right[0]

    return (default_level, default_right)
