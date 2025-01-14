import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook

from handlers.group_handlers import group_router
from handlers.private_handlers import private_router
# from middlewares.logging_middleware import LoggingMiddleware 
from middlewares.media_filter_middleware import MediaGroupFilterMiddleware
from middlewares.throttling_middleware import ThrottlingMiddleware
from utils.db import redis
from config import (GROUP_CHAT_MESSAGE_LIMIT, GROUP_CHAT_TIME_WINDOW_SECONDS, 
                    PRIVATE_CHAT_MESSAGE_LIMIT, PRIVATE_CHAT_TIME_WINDOW_SECONDS)


logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    load_dotenv()
    
    bot_token = os.getenv("TG_BOT_TOKEN")
    if not bot_token:
        exit("Specify TG_BOT_TOKEN env variable")
    
    bot = Bot(token=bot_token)
    
    dp = Dispatcher()
    dp.message.middleware(MediaGroupFilterMiddleware(redis=redis, 
                                                     expiry_seconds=60))
    dp.message.middleware(ThrottlingMiddleware(redis=redis,
                                               bot=bot,
                                               group_chat_message_limit=GROUP_CHAT_MESSAGE_LIMIT,
                                               private_chat_message_limit=PRIVATE_CHAT_MESSAGE_LIMIT,
                                               group_chat_time_window=GROUP_CHAT_TIME_WINDOW_SECONDS,
                                               private_chat_time_window=PRIVATE_CHAT_TIME_WINDOW_SECONDS))
    # dp.message.middleware(LoggingMiddleware())
    
    dp.include_router(group_router)
    dp.include_router(private_router)
    
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    asyncio.run(main())
