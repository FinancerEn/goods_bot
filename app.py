# Импорты Питона.
import asyncio
import os
from typing import Optional

# Импорты фреймворка.
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# Импорты Middleware для базы данных..
from aiogram.types import BotCommandScopeAllPrivateChats
# from middlewares.db import DataBaseSession
# from database.engine import create_db, drop_db, session_maker

from handlers.user_private import user_private_router
from handlers.handle_products import handle_products_router
from handlers.handle_payment import handle_payment_router

load_dotenv()

# ALLOWED_UPDATES = ["message", "edited_message", "callback_query"]

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения 'TOKEN' не задана.")

# db_url = os.getenv("DB_URL_SQLITE")

# db_url = os.getenv("DB_URL")
# Проверяем, что URL не пустой
# print(f"DB_URL загружен: {db_url}")
# if not db_url:
#     raise ValueError("Переменная окружения DB_URL не задана!")

GROUP_ID_ENV = os.getenv("GROUP_ID")
GROUP_ID: Optional[int] = (
    int(GROUP_ID_ENV) if GROUP_ID_ENV and GROUP_ID_ENV.isdigit() else None
)

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(handle_products_router)
dp.include_router(handle_payment_router)


# # Функции относящиеся к БД, (движку моделей из engine.py).
# # Если run_param=True, база удалится и создастся заново.
# # Иначе просто создаётся база, если её ещё нет.
# async def on_startup(bot):

#     run_param = False
#     if run_param:
#         await drop_db()

#     await create_db()


# Просто выводит сообщение при остановке бота.
async def on_shutdown(bot):
    print("бот лег")


async def main():
    # dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # 1. Подключение middleware (ПЕРВЫМ ДЕЛОМ!)
    # dp.update.middleware(DataBaseSession(session_pool=session_maker))

    # 4. Настройка бота
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())

    # 5. Запуск поллинга
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
