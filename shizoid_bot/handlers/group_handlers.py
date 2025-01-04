import logging
import random
from collections import defaultdict, deque
from aiogram import Router, Bot
from aiogram.types import Message, ChatMemberUpdated, Message
from aiogram.filters import (ChatMemberUpdatedFilter, Command, IS_MEMBER, 
                             IS_NOT_MEMBER)

from texts.bot_messages import (ADD_GROUP_EVENT_MESSAGE, 
                                LIMIT_MESSAGE_EXCEEDED, 
                                LIMIT_MESSAGE_NOT_EXCEEDED)
from texts.system_messages import (TEXT_TO_TEXT_SYSTEM_MESSAGE, 
                                   IMAGE_TO_TEXT_SYSTEM_MESSAGE)
from utils.db import redis
from services.openai_api import create_response
from utils.time_utils import format_ttl_flexible
from utils.helpers import check_limit
from filters.group_filters import *
from config import *

# TODO В redis
user_histories: defaultdict = defaultdict(lambda: deque(maxlen=CHAT_HISTORY_LENGTH))
logger = logging.getLogger(__name__)
group_router = Router()

async def get_message_text(message: Message) -> str:
    return message.text or message.caption


async def handle_photo(bot: Bot, message: Message) -> str:
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": IMAGE_TO_TEXT_SYSTEM_MESSAGE},
                {"type": "image_url", "image_url": {"url": file_url}}
            ]
        }
    ]
    model_response = await create_response(messages, "image_to_text")
    return f"<Описание изображения>{model_response}<Описание изображения>"


async def build_messages(system_message, 
                         user_message, 
                         history=None, 
                         image_description=""):
    if user_message is None:
        user_message  = ""
    
    messages = [{"role": "system", "content": system_message}]

    if history:
        for user_msg, bot_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
    
    full_user_message = image_description + user_message
    messages.append({"role": "user", "content": full_user_message})

    return messages


@group_router.message(IsGroupChatMessage(), Command("limit"))
async def cmd_limit(message: Message):
    user_id =  message.from_user.id
    allowed, ttl = await check_limit(user_id, redis=redis)
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
        

@group_router.message(IsGroupChatMessage(), 
                      IsBotReplyOrMention())
async def handle_mention_of_bot(message: Message, bot: Bot):
    if not ALLOW_REPLY_OR_MENTION:
        return
    
    if random.random() > REPLY_OR_MENTION_MESSAGE_REPLY_CHANCE:
        return
    
    user_message = await get_message_text(message)
    if (user_message and (len(user_message) > REPLY_OR_MENTION_MESSAGE_MAX_LENGTH) 
        or (not message.photo and (not user_message or len(user_message) < REPLY_OR_MENTION_MESSAGE_MIN_LENGTH))):
        return

    image_description = ""
    if message.photo and (not user_message 
                          or len(user_message) <= CAPTION_MAX_LENGTH):
        try:
            image_description = await handle_photo(bot, message)
        except Exception as e:
            logger.error(f"Error processing photo: {e}")

    user_id = message.from_user.id
    history = user_histories[user_id]
    messages = await build_messages(
        history=history,
        system_message=TEXT_TO_TEXT_SYSTEM_MESSAGE,
        user_message=user_message,
        image_description=image_description
    )
    try:
        model_response = await create_response(messages)
        await message.reply(model_response)
        
        history.append((user_message, model_response))

    except Exception as e:
        logger.error(f"Error processing reply or mention: {e}")


@group_router.message(IsForwardMessage(), 
                      ~PrivateMessage())
async def handle_forward_group_message(message: Message, bot: Bot):
    if random.random() > FORWARD_MESSAGE_REPLY_CHANCE:
        return
    
    user_message = await get_message_text(message)
    if (user_message and (len(user_message) > FORWARD_MESSAGE_MAX_LENGTH) 
        or (not message.photo and (not user_message or len(user_message) < FORWARD_MESSAGE_MIN_LENGTH))):
        return

    image_description = ""
    if message.photo and (not user_message 
                          or len(user_message) <= CAPTION_MAX_LENGTH):
        try:
            image_description = await handle_photo(bot, message)
        except Exception as e:
            logger.error(f"Error processing photo: {e}")
    
    messages = await build_messages(
        system_message=TEXT_TO_TEXT_SYSTEM_MESSAGE,
        user_message=user_message,
        image_description=image_description
    )
    try:
        model_response = await create_response(messages)
        await message.answer(model_response)

    except Exception as e:
        logger.error(f"Error processing forward message:) {e}")


@group_router.message(IsGroupChatMessage(), 
                      ~IsForwardMessage(),
                      ~IsBotReplyOrMention())
async def handle_group_message(message: Message, bot: Bot):
    if random.random() > COMMON_GROUP_MESSAGE_REPLY_CHANCE:
        return
    
    user_message = await get_message_text(message)
    if (user_message and (len(user_message) > COMMON_MESSAGE_MAX_LENGTH) 
        or (not message.photo and (not user_message or len(user_message) < COMMON_MESSAGE_MAX_LENGTH))):
        return
    
    image_description = ""
    if message.photo and (not user_message 
                          or len(user_message) <= CAPTION_MAX_LENGTH):
        try:
            image_description = await handle_photo(bot, message)
        except Exception as e:
            logger.error(f"Error processing photo: {e}")
            
    messages = await build_messages(
        system_message=TEXT_TO_TEXT_SYSTEM_MESSAGE,
        user_message=user_message,
        image_description=image_description
    )
    
    try:
        model_response = await create_response(messages)
        await message.reply(model_response)
        
        user_id = message.from_user.id
        history = user_histories[user_id]
        history.append((user_message, model_response))
            
    except Exception as e:
        logger.error(f"Error processing long message: {e}")
