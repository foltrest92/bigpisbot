import logging
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command('start'))
async def hello(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    kb = [
        [types.InlineKeyboardButton(text='Добавить бота в чат', url='https://t.me/bigpisbot?startgroup=start')]
    ]
    await message.answer(text='Бот работает в группах', reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))