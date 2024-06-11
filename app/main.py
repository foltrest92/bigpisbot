import os, sys
sys.path.append(os.getcwd())

import asyncio
from aiogram import Bot, Dispatcher, types
from app.config import settings
from app.routers.start import router as start_router

async def start_bot():
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
    await bot.set_my_commands(commands, types.BotCommandScopeDefault())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_bot())