from aiogram.filters import Filter
from aiogram.types import Message


class IsGroupChatMessage(Filter):
    async def __call__(self, message: Message) -> bool:
        is_group_message = message.chat.type in ["group", "supergroup"]
        return is_group_message


class IsBotReplyOrMention(Filter):
    async def __call__(self, message: Message) -> bool:
        bot = await message.bot.me()
        
        message_text = message.text or message.caption
        
        is_reply = message.reply_to_message and message.reply_to_message.from_user.id == bot.id
        
        if message_text is None:
            is_mention = False
        else:
            is_mention = f"@{bot.username}" in message_text
            
        return is_reply or is_mention
    

class MessageLength(Filter):
    def __init__(self, min_length: int = None, max_length: int = None):
        self.min_length = min_length
        self.max_length = max_length

    async def __call__(self, message: Message) -> bool:
        if not message.text and not message.caption:
            return False
        
        message_text = message.text or message.caption
        
        if self.min_length is not None and len(message_text) <= self.min_length:
            return False
        if self.max_length is not None and len(message_text) >= self.max_length:
            return False
        
        return True
    
    
class IsForwardMessage(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.forward_from or message.forward_from_chat
    
    
class PrivateMessage(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "private"
    