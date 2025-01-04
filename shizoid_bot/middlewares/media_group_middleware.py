import asyncio
import logging
from aiogram import BaseMiddleware
from aiogram.types import Message
from redis.asyncio import Redis

from exceptions.exceptions import CancelHandler

logger = logging.getLogger(__name__)

class MediaGroupFilterMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, expiry_seconds: int = 60):
        super().__init__()
        self.redis = redis
        self.expiry_seconds = expiry_seconds
        self.lock = asyncio.Lock()

    async def __call__(self, handler, event: Message, data: dict):
        media_group_id = event.media_group_id

        if not media_group_id:
            return await handler(event, data)

        async with self.lock:
            redis_key = f"media_group:{media_group_id}"
            exists = await self.redis.exists(redis_key)

            if exists:
                logger.debug(f"Пропуск сообщения {event.message_id} из media_group_id={media_group_id}")
                return
            else:
                await self.redis.set(redis_key, 1, ex=self.expiry_seconds)
                logger.debug(f"Обработка ПЕРВОГО сообщения {event.message_id} из media_group_id={media_group_id}")

        return await handler(event, data)