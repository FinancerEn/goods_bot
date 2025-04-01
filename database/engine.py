# Файл, ассинхронный движок ORM. Реализуем возможность работать с базой данных через models.
import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base

from dotenv import load_dotenv
load_dotenv()

# Получаем URL БД sqlite из .env
# db_url = os.getenv("DB_URL_SQLITE")

# Получаем URL БД postgres из .env
db_url = os.getenv("DB_URL")

# print(f"DB_URL загружен: {db_url}")

# Проверяем, что URL не пустой
# print(f"DB_URL загружен: {db_url}")
if not db_url:
    raise ValueError("Переменная окружения DB_URL не задана!")

# Создаем движок. Из .env импортируем "DB_URL" url БД и echo=True что бы все SQL запросы выводились в терминал.
engine = create_async_engine(db_url, echo=True)

# Создаем фабрику сессий. От которой мы берём сессии что бы делать запросы в БД.
# AsyncSession ассинхронный класс создания сессий.
# expire_on_commit=False что бы мы могли воспользоваться сессией повторно и она не закрывалась после коммита.
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Создаём или удаляем через ORM систему таблицы которые описанны в models.
# Когда вызывается Base.metadata.create_all, SQLAlchemy создаёт таблицы в базе.
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Если нужно удалить все таблицы которые были созданны.
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
