from datetime import datetime
import os, sys
sys.path.append(os.getcwd())

import locale
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, filename=f'log/{datetime.now().strftime("%y%m%d%H%M%S")}.log',
                    filemode='a', format="%(asctime)s %(levelname)s %(message)s")

import asyncio
from aiogram import Bot, Dispatcher, types
from app.config import settings
from app.routers.start import router as start_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app import planned

async def start_bot():
    logging.info('start_bot()')
    dp = Dispatcher()
    bot = Bot(settings.BOT_TOKEN)

    dp.include_router(start_router)

    commands = [
        types.BotCommand(command='dick', description='Вырастить пипису'),
        types.BotCommand(command='top', description='Топ 10 пипис'),
        types.BotCommand(command='stats', description='Статистика в картинке'),
        types.BotCommand(command='global_top', description='Глобальный топ'),
        types.BotCommand(command='help', description='Помощь'),
        types.BotCommand(command='buy', description='Покупка доп. попытки')
    ]

    scheduler = AsyncIOScheduler()
    scheduler.add_job(planned.reset, 'cron', hour=7, minute=30)
    logging.info('Job \'reset\' added')
    await bot.set_my_commands(commands, types.BotCommandScopeDefault())
    logging.info('commands setted')
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info('webhook deleted')
    logging.info('starting polling')
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.info('Start')
    locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
    asyncio.run(start_bot())