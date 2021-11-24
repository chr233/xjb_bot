from typing import List

from aiogram import types

from .base import BaseStorage

import aioredis

try:
    import ujson as json
except ImportError:
    import json


class RedisStorage(BaseStorage):
    def __init__(self, redis: aioredis.Redis, prefix: str, ttl: int):
        self._redis = redis
        self._prefix = prefix
        self._ttl = ttl

    def _get_media_group_handled_key(self, media_group_id: str) -> str:
        return f"{self._prefix}:{media_group_id}:handled"

    def _get_media_group_messages_key(self, media_group_id: str) -> str:
        return f"{self._prefix}:{media_group_id}:messages"

    async def set_media_group_as_handled(self, media_group_id: str) -> bool:
        return await self._redis.set(
            name=self._get_media_group_handled_key(media_group_id),
            value=1,
            ex=self._ttl,
            nx=True,
        )

    async def append_message_to_media_group(
        self, media_group_id: str, message: types.Message
    ):
        length = await self._redis.lpush(
            self._get_media_group_messages_key(media_group_id),
            json.dumps(message.to_python())
        )

        if length == 1:
            await self._redis.expire(
                name=self._get_media_group_messages_key(media_group_id),
                time=self._ttl,
            )

    async def get_media_group_messages(
        self, media_group_id: str
    ) -> List[types.Message]:
        raw_messages = await self._redis.lrange(
            name=self._get_media_group_messages_key(media_group_id),
            start=0,
            end=10
        )
        messages = [types.Message(**json.loads(m)) for m in raw_messages]
        messages.sort(key=lambda m: m.message_id)

        return messages

    async def delete_media_group(self, media_group_id: str):
        await self._redis.delete(
            self._get_media_group_handled_key(media_group_id),
            self._get_media_group_messages_key(media_group_id),
        )
