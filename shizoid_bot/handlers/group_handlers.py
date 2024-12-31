import logging
import random
from collections import defaultdict, deque
from aiogram import F, Router
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import invert_f, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from openai import OpenAIError

from texts.bot_messages import ADD_GROUP_EVENT_MESSAGE
from texts.system_message import SYSTEM_MESSAGE
from services.openai_api import create_response
from config import REPLY_CHANCE, CHAT_HISTORY_LENGTH
from filters.group_filters import *


user_histories: defaultdict = defaultdict(lambda: deque(maxlen=CHAT_HISTORY_LENGTH))
logger = logging.getLogger(__name__)
group_router = Router()

@group_router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER << IS_NOT_MEMBER))
async def bot_added_to_group(event: ChatMemberUpdated):
    if event.new_chat_member.user.id == (await event.bot.me()).id:
        await event.bot.send_message(
            event.chat.id,
            ADD_GROUP_EVENT_MESSAGE)


@group_router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER << IS_NOT_MEMBER))
async def bot_added_to_group(event: ChatMemberUpdated):
    if event.new_chat_member.user.id == (await event.bot.me()).id:
        await event.bot.send_message(
            event.chat.id,
            ADD_GROUP_EVENT_MESSAGE)
        

@group_router.message(IsGroupChatMessage(), IsReplyOrMention())
async def handle_mention_of_bot(message: Message):
    user_id = message.from_user.id
    user_message = message.text
    history = user_histories[user_id]
    try:
        messages = [{"role": "system", "content": SYSTEM_MESSAGE},] 

        for user_msg, bot_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
        
        messages.append({"role": "user", "content": user_message})
        
        model_response = create_response(messages)
        
        await message.reply(model_response)
        
        history.append((user_message, model_response))
        
    except OpenAIError as e:
        logger.error(f"OpenAI error: {e}")
    except ValueError as e:
        logger.error(f"{e}")


@group_router.message(IsGroupChatMessage(), 
                      IsLongMessage(min_length=CHAT_HISTORY_LENGTH), 
                      invert_f(IsReplyOrMention()))
async def handle_long_group_message(message: Message):
    try:
        if random.random() <= REPLY_CHANCE:
            user_id = message.from_user.id
            user_message = message.text
            
            messages = [{"role": "system", "content": SYSTEM_MESSAGE},
                        {"role": "user", "content": user_message}] 
            
            model_response = create_response(messages)
            await message.reply(model_response)
            
            history = user_histories[user_id]
            history.append((user_message, model_response))
            
    except OpenAIError as e:
        logger.error(f"OpenAI error: {e}")
    except ValueError as e:
        logger.error(f"{e}")