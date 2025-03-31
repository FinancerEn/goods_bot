import os
from typing import Optional
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, CallbackQuery, Message
from filters.chat_types import ChatTypeFilter

from dotenv import load_dotenv

from text_message import text
from kbds import inline

load_dotenv()

GROUP_ID_ENV = os.getenv('GROUP_ID')
GROUP_ID: Optional[int] = (
    int(GROUP_ID_ENV) if GROUP_ID_ENV and GROUP_ID_ENV.isdigit() else None
)

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: Message):
    photo = FSInputFile('images/start.webp')
    await message.answer_photo(photo)
    await message.answer(
        text.main_text, reply_markup=inline.inline_main
    )
