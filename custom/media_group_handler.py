'''
# @Author       : Chr_
# @Date         : 2021-11-03 00:28:52
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-24 23:39:50
# @Description  : 自定义消息处理器
'''

import asyncio
import aioredis
from functools import wraps
from typing import Callable, Optional

from aiogram import types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage as AiogramMemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2 as AiogramRedis2Storage
from aiogram.dispatcher import FSMContext

from models.user import Users

from .storages.base import BaseStorage
from .storages.memory import MemoryStorage
from .storages.redis import RedisStorage


async def _get_storage_from_state(state: FSMContext, prefix, ttl):
    storage_type = type(state.storage)
    if storage_type is AiogramMemoryStorage:
        return MemoryStorage(data=state.storage.data, prefix=prefix)
    elif storage_type is AiogramRedis2Storage:
        pool = aioredis.ConnectionPool.from_url(
            "redis://localhost:6379", decode_responses=True
        )
        redis = aioredis.Redis(connection_pool=pool)
        return RedisStorage(redis=redis, prefix=prefix, ttl=ttl)
    else:
        raise ValueError(f"{storage_type} is unsupported storage")


async def _on_media_group_received(
    media_group_id: str,
    storage: BaseStorage,
    user: Users,
    callback,
    *args,
    **kwargs,
):
    messages = await storage.get_media_group_messages(media_group_id)
    await storage.delete_media_group(media_group_id)

    return await callback(messages, user, *args, **kwargs)


def media_group_handler(
    func: Optional[Callable] = None,
    receive_timeout: int = 2,
    ttl: int = 5,
    storage_prefix: str = "mgroup",
    storage_driver: Optional[BaseStorage] = None,
):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(message: types.Message, *args, **kwargs):
            if message.media_group_id is None:
                raise ValueError("Not a media group message")

            event_loop = asyncio.get_event_loop()

            if storage_driver is not None:
                storage = storage_driver
            else:
                state = Dispatcher.get_current().current_state()
                storage = await _get_storage_from_state(
                    state, prefix=storage_prefix, ttl=ttl
                )

            if await storage.set_media_group_as_handled(message.media_group_id):
                event_loop.call_later(
                    receive_timeout,
                    asyncio.create_task,
                    _on_media_group_received(
                        message.media_group_id, storage, message.user, handler, *args, **kwargs
                    ),
                )

            await storage.append_message_to_media_group(message.media_group_id, message)

        return wrapper

    if callable(func):
        return decorator(func)

    return decorator
