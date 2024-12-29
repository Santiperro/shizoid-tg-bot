import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers.group_handlers import group_router
from handlers.private_handlers import private_router


async def main():
    load_dotenv()
    
    bot_token = os.getenv("TG_BOT_TOKEN")
    if not bot_token:
        exit("Specify TG_BOT_TOKEN env variable")
    
    bot = Bot(token=bot_token)
    
    dp = Dispatcher()
    dp.include_router(group_router)
    dp.include_router(private_router)
    
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO)
    asyncio.run(main())
