from aiogram import F, Router
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, invert_f
from openai import OpenAIError
import logging

from texts.bot_messages import ADD_GROUP_EVENT_MESSAGE
from services.openai_api import create_response
from filters.group_filters import *


logger = logging.getLogger(__name__)
group_router = Router()

@group_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=True))
async def bot_added_to_group(event: ChatMemberUpdated):
    if event.new_chat_member.user.id == (await event.bot.me()).id:
        await event.bot.send_message(
            event.chat.id,
            ADD_GROUP_EVENT_MESSAGE)
        
        
@group_router.message(IsGroupChatMessage(), IsReplyOrMention())
async def handle_mention_of_bot(message: Message):
    try: 
        model_response = create_response(message.text)
        await message.reply(model_response)
    except OpenAIError as e:
        logger.error(f"OpenAI error: {e}")
            

@group_router.message(IsGroupChatMessage(), IsLongMessage(min_length=100), invert_f(IsReplyOrMention()))
async def handle_long_group_message(message: Message):
    try:
        model_response = create_response(message.text)
        await message.reply(model_response)
    except OpenAIError as e:
        logger.error(f"OpenAI error: {e}")