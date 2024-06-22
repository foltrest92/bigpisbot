import logging
import os
from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from app.config import settings
from app.dao.promos import PromoDAO
from app.dao.sizes import SizesDAO

router = Router()

@router.message(Command('log'))
async def log(message: types.Message):
    logging.info('ADMIN: get log, user_id:'+ str(message.from_user.id))
    if message.from_user.id != settings.ADMIN_TELEGRAM_ID:
        return
    filenames = os.listdir('log')
    filenames.sort()
    await message.answer_document(types.FSInputFile('log/'+filenames[-1]))

@router.message(Command('reset'))
async def reset(message: types.Message):
    logging.info('ADMIN: reset, user_id:'+str(message.from_user.id))
    if message.from_user.id != settings.ADMIN_TELEGRAM_ID:
        return
    await SizesDAO.reset()
    await message.answer('Выполнено')

@router.message(Command('newpromo'))
async def newpromo(message: types.Message, command: CommandObject):
    logging.info('ADMIN: new promo ('+message.text+'), user_id:'+str(message.from_user.id))
    if message.from_user.id != settings.ADMIN_TELEGRAM_ID:
        return
    if command.args == None:
        logging.info('Нет аргументов')
        await message.answer('Нет аргументов')
        return
    args = command.args.split()
    if args!=2:
        await message.answer('Ошибка ввода')
        logging.info('Promo isnot added.')
        return
    await PromoDAO.add(
        code=args[0],
        uses=int(args[1])
    )
    logging.info('Promo added')

@router.message(Command('updatepromo'))
async def updatepromo(message: types.Message, command: CommandObject):
    logging.info('ADMIN: update promo ('+message.text+'), user_id:'+str(message.from_user.id))
    if message.from_user.id != settings.ADMIN_TELEGRAM_ID:
        return
    if command.args == None:
        logging.info('Нет аргументов')
        await message.answer('Нет аргументов')
        return
    args = command.args.split()
    if args!=2:
        await message.answer('Ошибка ввода')
        logging.info('Promo isnot added.')
    await PromoDAO.update(
        code=args[0],
        uses=int(args[1])
    )
    logging.info('Promo added')

@router.message(Command('version'))
async def version(message: types.Message):
    logging.info('ADMIN: version ('+message.text+'), user_id:'+str(message.from_user.id))
    if message.from_user.id != settings.ADMIN_TELEGRAM_ID:
        return
    await message.answer(settings.VERSION)