import logging
import types
from aiogram import Router
from aiogram.filters import Command

router = Router()



@router.message(Command('help'))
async def help(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    await message.answer('Команды бота:\n/dick — Вырастить/уменьшить пипису\n/top — Топ 10 пипис чата\n/stats — Статистика в виде картинки\n/global_top — Глобальный топ 10 игроков\n/buy — Покупка доп. попыток\n\nКонтакты:')