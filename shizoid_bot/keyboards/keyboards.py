from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardButton, InlineKeyboardMarkup)

from texts.bot_buttons import *
from config import DEFAULT_BOT_RIGHTS


def create_add_bot_keyboard(bot_username: str) -> InlineKeyboardMarkup:
    
    admin_rights = "+".join(DEFAULT_BOT_RIGHTS)
    
    add_link = f"https://t.me/{bot_username}?startgroup=true&admin={admin_rights}"
    
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
