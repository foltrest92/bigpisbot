import logging

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

logging.info('MODE: ' + settings.MODE)

# Настройка БД и токена в зависимости от типа запуска
if settings.MODE == "TEST":
    DATABASE_URL = f'postgresql+asyncpg://{settings.TEST_DB_USER}:{settings.TEST_DB_PASS}@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}'
    DATABASE_PARAMS = {'poolclass': NullPool}
    settings.BOT_TOKEN = settings.TEST_BOT_TOKEN
    settings.PAYMENT_TOKEN = settings.DEV_PAYMENT_TOKEN
elif settings.MODE == 'DEV':
    DATABASE_URL = f'postgresql+asyncpg://{settings.DEV_DB_USER}:{settings.DEV_DB_PASS}@{settings.DEV_DB_HOST}:{settings.DEV_DB_PORT}/{settings.DEV_DB_NAME}'
    DATABASE_PARAMS = {}
    settings.BOT_TOKEN = settings.DEV_BOT_TOKEN
    settings.PAYMENT_TOKEN = settings.DEV_PAYMENT_TOKEN
elif settings.MODE == 'PROD':
    DATABASE_URL = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
    DATABASE_PARAMS = {}
    settings.BOT_TOKEN = settings.PROD_BOT_TOKEN
    settings.PAYMENT_TOKEN = settings.PROD_PAYMENT_TOKEN

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
logging.info('created async engine')

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
logging.info('created session maker')

class Base(DeclarativeBase):
    pass
