from aiogram.filters import Filter
from aiogram.types import Message


class IsGroupChatMessage(Filter):
    async def __call__(self, message: Message) -> bool:
        is_group_message = message.chat.type in ["group", "supergroup"]
        return is_group_message


class IsBotReplyOrMention(Filter):
    async def __call__(self, message: Message) -> bool:
        bot_user = await message.bot.me()
        
        is_reply = message.reply_to_message and message.reply_to_message.from_user.id == bot_user.id
        
        is_mention = message.entities and any(
            entity.type == 'mention' and f"@{bot_user.username}" in message.text
            for entity in message.entities
        )
        
        return is_reply or is_mention
    

class IsLongMessage(Filter):
    def __init__(self, min_length: int):
        self.min_length = min_length

    async def __call__(self, message: Message) -> bool:
        return ((message.text and len(message.text) > self.min_length) 
                or (message.caption and len(message.caption) > self.min_length))
    
    
class IsForwardMessage(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.forward_from or message.forward_from_chat
    
    
class PrivateMessage(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "private"
    