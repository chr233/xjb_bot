'''
# @Author       : Chr_
# @Date         : 2021-10-29 15:02:59
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-29 15:23:28
# @Description  : 初始化数据库
'''

from loguru import logger
from tortoise import Tortoise

from config import CFG


async def init_orm(*args, **kwargs):
    await Tortoise.init(
        db_url=CFG.DB_URL,
        modules={
            'models': [
                'models.badge',
                'models.level',
                'models.post',
                'models.rating',
                'models.reason',
                'models.right',
                'models.tag',
                'models.user',
            ]
        }
    )
    logger.info("Tortoise-ORM started")
    if CFG.Generate_Schemas:
        logger.info("Tortoise-ORM generating schema")
        await Tortoise.generate_schemas()


async def close_orm(*args, **kwargs) -> None:
    await Tortoise.close_connections()
    logger.info("Tortoise-ORM shutdown")
