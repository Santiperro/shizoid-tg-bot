import asyncio
import logging
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from aiogram.filters import Command
from redis.asyncio import Redis

from exceptions.exceptions import CancelHandler
from filters.group_filters import IsPrivateMessage, IsGroupChatMessage

logger = logging.getLogger(__name__)

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, 
                 bot: Bot, 
                 group_chat_message_limit: int,
                 private_chat_message_limit: int, 
                 group_chat_time_window: int,
                 private_chat_time_window: int):
        super().__init__()
        self.redis = redis
        self.bot = bot
        self.group_chat_message_limit = group_chat_message_limit
        self.private_chat_message_limit = private_chat_message_limit
        self.group_chat_time_window = group_chat_time_window
        self.private_chat_time_window = private_chat_time_window
        self.lock = asyncio.Lock()

    async def __call__(self, handler, event: Message, data: dict):
        user = event.from_user
        chat = event.chat
        
        if not user or await Command("limit")(event, self.bot):
            return await handler(event, data)

        if await IsPrivateMessage()(event):
            try:
                await self._handle_rate_limit(
                    event, 
                    f"user_private_chat_requests:{user.id}",
                    self.private_chat_message_limit,
                    self.private_chat_time_window
                )
            except CancelHandler:
                return

        elif await IsGroupChatMessage()(event):
            try:
                await self._handle_rate_limit(
                    event, 
                    f"group_chat:{chat.id}:user:{user.id}",
                    self.group_chat_message_limit,
                    self.group_chat_time_window
                )
            except CancelHandler:
                return

        return await handler(event, data)

    async def _handle_rate_limit(self, message: Message, 
                                 redis_key: str, 
                                 limit: int, 
                                 time_window: int):
        user_id = message.from_user.id

        async with self.lock:
            current_count = await self.redis.get(redis_key)

            if current_count and int(current_count) >= limit:
                ttl = await self.redis.ttl(redis_key)
                logger.info(
                    f"User {user_id} exceeded message limit. "
                    f"TTL: {ttl} seconds."
                )
                raise CancelHandler

            pipeline = self.redis.pipeline()
            pipeline.incr(redis_key)
            pipeline.expire(redis_key, time_window)
            await pipeline.execute()