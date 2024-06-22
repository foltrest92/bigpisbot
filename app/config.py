
from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODE: Literal['PROD', 'DEV', 'TEST']

    BOT_TOKEN: str

    ADMIN_TELEGRAM_ID: int

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str
    
    DEV_DB_HOST: str
    DEV_DB_PORT: int
    DEV_DB_USER: str
    DEV_DB_PASS: str
    DEV_DB_NAME: str



    class Config:
        env_file = '.env'

settings = Settings()