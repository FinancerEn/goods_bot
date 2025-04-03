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
    run_param = False
    if run_param:
        await drop_db()
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
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
# ______________________________________________________


# async def on_startup(bot):
#     await create_db()
#     print("Бот запущен!")

# async def main():
#     # Инициализация логирования запуска
#     print("=== Запуск бота ===")
#     print(f"GROUP_ID: {GROUP_ID} (тип: {type(GROUP_ID)})")
    
#     # Регистрация обработчиков
#     dp.startup.register(on_startup)
#     dp.update.middleware(DataBaseSession(session_pool=session_maker))

#     # Очистка перед запуском
#     print("Очистка вебхука...")
#     await bot.delete_webhook(drop_pending_updates=True)
    
#     # Загрузка администраторов
#     print("\nЗагрузка списка администраторов...")
#     if GROUP_ID:
#         try:
#             print(f"Запрашиваем администраторов для группы {GROUP_ID}...")
#             admins = await bot.get_chat_administrators(GROUP_ID)
#             bot.my_admins_list = [
#                 admin.user.id 
#                 for admin in admins 
#                 if admin.status in ["creator", "administrator"]
#             ]
#             print(f"✅ Успешно загружены админы ({len(bot.my_admins_list)}): {bot.my_admins_list}")
#         except Exception as e:
#             print(f"❌ Критическая ошибка загрузки админов: {e}")
#             print("⚠️ Админ-панель будет недоступна!")
#             bot.my_admins_list = []
#     else:
#         print("⚠️ GROUP_ID не задан, админка отключена")
#         bot.my_admins_list = []

#     # Запуск бота
#     print("\nЗапуск бота в режиме поллинга...")
#     try:
#         await dp.start_polling(bot)
#     except Exception as e:
#         print(f"❌ Фатальная ошибка: {e}")
#     finally:
#         print("Завершение работы...")
#         await bot.session.close()
#     print("Бот остановлен")

# if __name__ == "__main__":
#     asyncio.run(main())
# __________________________________________________


# что бы совершить логирование раскоментировать код ниже и заменить main на этот код
# async def main():
#     bot = Bot(token=TOKEN)
#     dp = Dispatcher()

#     # 1. Подключение middleware ПЕРВЫМ ДЕЛОМ
#     dp.update.outer_middleware(DataBaseSession(session_pool=session_maker))

#     # 2. Регистрация роутеров
#     dp.include_router(user_private_router)
#     dp.include_router(handle_products_router)
#     dp.include_router(handle_payment_router)

#     # 3. Регистрация обработчиков startup/shutdown
#     dp.startup.register(on_startup)
#     dp.shutdown.register(on_shutdown)

#     # 4. Настройка бота
#     await bot.delete_webhook(drop_pending_updates=True)
#     await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())

#     # 5. Запуск поллинга с обработкой SSL ошибок
#     try:
#         await dp.start_polling(bot)
#     except Exception as e:
#         logger.error(f"Ошибка при запуске: {e}")
#     finally:
#         await bot.session.close()

# if __name__ == "__main__":
#     # Для Windows нужно установить политику event loop
#     if os.name == 'nt':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         logger.info("Бот остановлен вручную")
