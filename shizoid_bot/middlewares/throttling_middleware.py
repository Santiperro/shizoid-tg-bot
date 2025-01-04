import asyncio
import logging
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from redis.asyncio import Redis

from exceptions.exceptions import CancelHandler
from filters.group_filters import IsBotReplyOrMention

logger = logging.getLogger(__name__)

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, bot: Bot, message_limit: int, time_window: int):
        super().__init__()
        self.redis = redis
        self.bot = bot
        self.message_limit = message_limit
        self.time_window = time_window
        self.lock = asyncio.Lock()
        self.is_reply_or_mention = IsBotReplyOrMention()

    async def __call__(self, handler, event: Message, data: dict):
        user = event.from_user
        if not user:
            return await handler(event, data)

        user_id = user.id
        redis_key = f"user_requests:{user_id}"

        async with self.lock:
            if not await self.is_reply_or_mention(event):
                return await handler(event, data)
            
            current_count = await self.redis.get(redis_key)
            if current_count and int(current_count) >= self.message_limit:
                ttl = await self.redis.ttl(redis_key)
                logger.info(f"User {user_id} exceeded message limit. TTL: {ttl} seconds.")
                return

            pipeline = self.redis.pipeline()
            pipeline.incr(redis_key)
            pipeline.expire(redis_key, self.time_window)
            await pipeline.execute()

        return await handler(event, data)