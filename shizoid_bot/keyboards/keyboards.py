from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardButton, InlineKeyboardMarkup)

from texts.bot_buttons import *


def create_add_bot_keyboard(bot_username: str) -> InlineKeyboardMarkup:
    
    # TODO В конфиг
    default_rights = [
        # "promote_members",
        # "delete_messages",
        # "restrict_members",
        # "invite_users",
        "pin_messages",
        # "manage_video_chats",
        # "manage_call",
        # "manage_topics",
        # "anonymous",
        # "add_admins",
        # 'post_stories',
        # 'delete_stories'
    ]
    
    admin_rights_str = "+".join(default_rights)
    
    add_link = f"https://t.me/{bot_username}?startgroup=true&admin={admin_rights_str}"
    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ADD_BOT_INLINE_BUTTON,
                    url=add_link
                )
            ]
        ]
    )


main_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=ADD_BOT_BUTTON)],
        [KeyboardButton(text=HELP_BUTTON)]],
    resize_keyboard=True,
    input_field_placeholder="")
