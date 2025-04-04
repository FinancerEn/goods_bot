import asyncio
import os
# import logging
# from typing import Optional
from aiogram import Dispatcher
from filters.config import TOKEN, GROUP_ID
from filters.bot import CustomBot
from dotenv import load_dotenv
from aiogram.types import BotCommandScopeAllPrivateChats
from middlewares.db import DataBaseSession
from database.engine import create_db, drop_db, session_maker

# Импорты роутеров
from handlers.user_private import user_private_router
from handlers.handle_products import handle_products_router
from handlers.handle_payment import handle_payment_router
from handlers.admin_private import admin_router

# # что бы совершить логирование раскоментировать код ниже
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения 'TOKEN' не задана.")

db_url = os.getenv("DB_URL")
# что бы совершить логирование раскоментировать код ниже
# logger.info(f"DB_URL загружен: {db_url}")

bot = CustomBot(token=TOKEN)
bot.my_admins_list = []
dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(handle_products_router)
dp.include_router(handle_payment_router)
dp.include_router(admin_router)


async def on_startup(bot):
    # Раскоментировать если нужно обновить модели,
    # только закоментировать после 1 загрузки.
    # await drop_db()

    await create_db()
    print("Бот запущен!")


async def on_shutdown(bot):
    print('Бот лёг')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    # Реализуем наш Middleware слой.
    # Теперь в каждый хендлер нашего проекта будет пробрасываться сессия.
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())

    # Обновляем список админов перед стартом бота
    if GROUP_ID:
        admins_list = await bot.get_chat_administrators(GROUP_ID)
        bot.my_admins_list = [member.user.id for member in admins_list if member.status in ["creator", "administrator"]]

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
