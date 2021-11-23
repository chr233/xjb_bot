'''
# @Author       : Chr_
# @Date         : 2021-10-29 15:02:59
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-23 10:55:27
# @Description  : 数据库相关
'''

from loguru import logger
from tortoise import Tortoise

from config import CFG

async def init_orm(*args, **kwargs):
    '''
    初始化数据库
    '''
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
    '''
    关闭数据库
    '''
    await Tortoise.close_connections()
    logger.info("Tortoise-ORM shutdown")
