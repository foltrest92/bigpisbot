

from datetime import datetime
import logging
import os
import random
from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from app.daos import PromoDAO, SizedDAO
import matplotlib.pyplot as plt



router = Router()

variants = [-10,
            -9, 
            -8,
            -7, -7, 
            -6, -6,
            -5, -5,
            -4, -4, -4,
            -3, -3, -3,
            -2, -2, -2,
            -1, -1, -1,
            0,
            1, 1, 1, 1, 1,
            2, 2, 2, 2, 2, 2,
            3, 3, 3, 3, 3, 3, 3,
            4, 4, 4, 4, 4, 4, 4, 4,
            5, 5, 5, 5, 5, 5, 5, 5, 
            6, 6, 6, 6, 6, 6, 6, 6,
            7, 7, 7, 7, 7, 7,
            8, 8, 8, 8,
            9, 9, 9,
            10, 10]


@router.message(Command('start'))
async def hello(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    kb = [
        [types.InlineKeyboardButton(text='Добавить бота в чат', url='https://t.me/bigpisbot?startgroup=start')]
    ]
    await message.answer(text='Бот работает в группах', reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

@router.message(Command('dick'))
async def dick(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    if message.chat.id > 0:
        await message.answer('Бот работает только в чате')
        return
    
    row = await SizedDAO.find_one_or_none(chat_id=message.chat.id, user_id=message.from_user.id)
    if row is None:
        logging.debug('New user in chat')
        row = await SizedDAO.add(chat_id=message.chat.id, user_id=message.from_user.id)

    if row.isUpdated:
        tops = await SizedDAO.find_all(chat_id = message.chat.id)
        number = 1
        for key, top in enumerate(tops):
            if top.user_id != message.from_user.id:
                continue
            number = key + 1
            break
        await message.answer(text=f'<a href="{message.from_user.url}">{message.from_user.first_name}</a>, ты уже играл.\nСейчас он равен {row.size} см.\nТы занимаешь {number} место в топе.\nСледующая попытка завтра.', parse_mode='HTML')
        return
    
    step = variants[random.randint(0, len(variants)-1)]
    size = row.size + step
    await SizedDAO.update(chat_id=message.chat.id, user_id=message.from_user.id, size = size, isUpdated = True, name = message.from_user.first_name)

    tops = await SizedDAO.find_all(chat_id = message.chat.id)
    number = 1
    for key, top in enumerate(tops):
        if top.user_id != message.from_user.id:
            continue
        number = key + 1
        break

    if step >= 0:
        await message.answer(text=f'<a href="{message.from_user.url}">{message.from_user.first_name}</a>, твой писюн вырос на {step} см.\nСейчас он равен {size} см.\nТы занимаешь {number} место в топе.\nСледующая попытка завтра!', parse_mode='HTML')
    elif step < 0:
        await message.answer(text=f'<a href="{message.from_user.url}">{message.from_user.first_name}</a>, твой писюн сократился на {step} см.\nСейчас он равен {size} см.\n Ты занимаешь {number} место в топе.\nСледующая попытка завтра!', parse_mode='HTML')
    

@router.message(Command('top'))
async def top(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    if message.chat.id > 0:
        await message.answer('Бот работает только в чате')
        return
    
    msg = 'Топ 10 игроков:\n\n'

    top = await SizedDAO.get_top(chat_id=message.chat.id)
    for key, row in enumerate(top):
        msg += f'{key+1}|{row.name} - {row.size} см.\n'
     
    await message.answer(msg)

@router.message(Command('top'))
async def top(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    if message.chat.id > 0:
        await message.answer('Бот работает только в чате')
        return
    
    msg = 'Топ 10 игроков:\n\n'

    top = await SizedDAO.get_top(chat_id=message.chat.id)
    for key, row in enumerate(top):
        msg += f'{key+1}|{row.name} - {row.size} см.\n'
     
    await message.answer(msg)

@router.message(Command('global_top'))
async def global_top(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    
    msg = 'Топ 10 игроков:\n\n'

    top = await SizedDAO.get_top()
    for key, row in enumerate(top):
        msg += f'{key+1}|{row.name} - {row.size} см.\n'
     
    await message.answer(msg)

@router.message(Command('help'))
async def help(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    await message.answer('Команды бота:\n/dick — Вырастить/уменьшить пипису\n/top — Топ 10 пипис чата\n/stats — Статистика в виде картинки\n/global_top — Глобальный топ 10 игроков\n/buy — Покупка доп. попыток\n\nКонтакты:')


@router.message(Command('promo'))
async def promo(message: types.Message, command: CommandObject):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    if message.chat.id < 0:
        await message.answer('Команда работает только в лс')
        return
    if not command.args:
        await message.answer('Нужно ввести промокод\n/promo ПРОМОКОД')
        return
    is_used = await PromoDAO.use(command.args.strip())
    if is_used:
        await message.answer('Промокод применен, введите /dick в беседе')
    else:
        await message.answer('Промокод не существует или закончился')


@router.message(Command('stats'))
async def stats(message: types.Message, ):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    if message.chat.id > 0:
        await message.answer('Бот работает только в чате')
        return
    
    msg = 'Топ 10 игроков:\n\n'

    top = await SizedDAO.get_top(chat_id=message.chat.id)
    parts = []
    parts_labels = []
    for row in top:
        if row.size > 0:
            parts.append(row.size)
            parts_labels.append(f'{row.name} {row.size} см')
    
    filename = f"figs/{message.chat.id}_{datetime.now().strftime('%d%m%y_%H%M')}.png"
    if not os.path.exists(filename):
        logging.debug('Creating file: '+ filename)
        plt.pie(parts, labels=parts_labels)
        plt.title('Статистика '+ message.chat.title)
        # plt.legend(parts_labels, loc='upper right')
        plt.savefig(filename)
     
    await message.answer_photo(types.FSInputFile(filename))