import logging
import random
import datetime
from collections import defaultdict, deque
from aiogram import F, Router
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import (invert_f, ChatMemberUpdatedFilter, Command, 
                             IS_MEMBER, IS_NOT_MEMBER)

from texts.bot_messages import (ADD_GROUP_EVENT_MESSAGE, 
                                LIMIT_MESSAGE_EXCEEDED, 
                                LIMIT_MESSAGE_NOT_EXCEEDED)
from texts.system_message import SYSTEM_MESSAGE
from services.openai_api import create_response
from utils.time_utils import format_ttl_flexible
from config import REPLY_CHANCE, CHAT_HISTORY_LENGTH, REPLY_MESSAGE_LENGTH
from filters.group_filters import *
from utils.rate_limiter import is_request_allowed, check_limit


user_histories: defaultdict = defaultdict(lambda: deque(maxlen=CHAT_HISTORY_LENGTH))
logger = logging.getLogger(__name__)
group_router = Router()

@group_router.message(IsGroupChatMessage(), Command("limit"))
async def cmd_limit(message: Message):
    user_id =  message.from_user.id
    allowed, ttl = await check_limit(user_id)
    if allowed:
        await message.reply(LIMIT_MESSAGE_NOT_EXCEEDED)
    else: 
        await message.reply(LIMIT_MESSAGE_EXCEEDED.format(
            format_ttl_flexible(ttl)))


@group_router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER << IS_NOT_MEMBER))
async def bot_added_to_group(event: ChatMemberUpdated):
    if event.new_chat_member.user.id == (await event.bot.me()).id:
        await event.bot.send_message(
            event.chat.id,
            ADD_GROUP_EVENT_MESSAGE)
        

@group_router.message(IsGroupChatMessage(), IsBotReplyOrMention())
async def handle_mention_of_bot(message: Message):
    user_id = message.from_user.id
    
    allowed, ttl = await is_request_allowed(user_id)
    if not allowed:
        return

    user_message = message.text
    history = user_histories[user_id]
    
    try:
        messages = [{"role": "system", "content": SYSTEM_MESSAGE},] 

        for user_msg, bot_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
        
        messages.append({"role": "user", "content": user_message})
        
        model_response = await create_response(messages)
        await message.reply(model_response)
        
        history.append((user_message, model_response))
        
    except Exception as e:
        logger.error(f"Error processing mention: {e}")
    

@group_router.message(IsGroupChatMessage(), 
                      IsLongMessage(min_length=REPLY_MESSAGE_LENGTH), 
                      invert_f(IsBotReplyOrMention()))
async def handle_long_group_message(message: Message):
    try:
        if random.random() <= REPLY_CHANCE:
            user_id = message.from_user.id
            user_message = message.text
            
            messages = [{"role": "system", "content": SYSTEM_MESSAGE},
                        {"role": "user", "content": user_message}] 
            
            model_response = await create_response(messages)
            await message.reply(model_response)
            
            history = user_histories[user_id]
            history.append((user_message, model_response))
            
    except Exception as e:
        logger.error(f"Error processing long message: {e}")