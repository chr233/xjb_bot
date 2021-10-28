'''
# @Author       : Chr_
# @Date         : 2021-10-27 13:12:21
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-28 20:10:32
# @Description  : 
'''

import asyncio
import sys
from loguru import logger

from aiogram.dispatcher import filters
from aiogram.types.message import ContentType
from aiogram import Bot, Dispatcher, executor, types, md

from tortoise import run_async, Tortoise

from config import CFG

# print(CFG)

API_TOKEN = CFG.Bot_Token


bot = Bot(token=CFG.Bot_Token)
dp = Dispatcher(bot)


@dp.message_handler(content_types=ContentType.ANY)
async def echo(message: types.Message):
    print(message.content_type)

    media = types.MediaGroup()

    if message.content_type == ContentType.PHOTO:
        for i in message.photo:
            print(i.file_id)

    await message.reply("message.text")


def startup(generate_schemas: bool = False):
    '''启动函数'''
    async def init_orm(dp) -> None:  # pylint: disable=W0612
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
        if generate_schemas:
            logger.info("Tortoise-ORM generating schema")
            await Tortoise.generate_schemas()

    async def close_orm(dp) -> None:  # pylint: disable=W0612
        await Tortoise.close_connections()
        logger.info("Tortoise-ORM shutdown")

    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=init_orm,
        on_shutdown=close_orm
    )


if __name__ == '__main__':
    startup(generate_schemas=False)
