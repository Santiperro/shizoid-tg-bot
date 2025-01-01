from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards.keyboards import (main_keyboard as main_kb, 
                                  create_add_bot_keyboard)
from texts.bot_messages import *
from texts.bot_buttons import *


private_router = Router()

def is_private_chat(message: Message) -> bool:
    return message.chat.type == "private"


@private_router.message(CommandStart(), 
                        lambda message: is_private_chat(message))
async def cmd_start(message: Message):
    await message.answer(START_MESSAGE, 
                        reply_markup=main_kb)
    

@private_router.message(lambda message: is_private_chat(message) 
                        and message.text 
                        and (message.text == HELP_BUTTON 
                            or message.text.lower() == '/help'))
async def cmd_help(message: Message):
    await message.answer(HELP_MESSAGE,
                         reply_markup=main_kb)


@private_router.message(lambda message: is_private_chat(message)
                        and message.text
                        and message.text == ADD_BOT_BUTTON)
async def initiate_group_selection(message: Message):
    
    bot_username = (await message.bot.me()).username
    
    add_bot_kb = create_add_bot_keyboard(bot_username)

    await message.answer(
        ADD_BOT_TIP_MESSAGE,
        reply_markup=add_bot_kb)


@private_router.message(lambda message: is_private_chat(message) 
                        and message.text)
async def handle_default_text(message: Message):
    await message.answer(NOT_COMMAND_MESSAGE)