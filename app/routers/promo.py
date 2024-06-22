import logging
from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from app.dao.promos import PromoDAO

router = Router()

@router.message(Command('promo'))
async def promo(message: types.Message, command: CommandObject):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    if message.chat.id < 0:
        await message.answer('Команда работает только в лс')
        return
    if not command.args:
        await message.answer('Нужно ввести промокод\n/promo ПРОМОКОД')
        return
    is_used = await PromoDAO.use(command.args.strip(), message.from_user.id)
    if is_used:
        await message.answer('Промокод применен, введите /dick в беседе')
    else:
        await message.answer('Промокод не существует, уже использовал или закончился')