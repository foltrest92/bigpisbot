from datetime import datetime
import logging
import os
from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from matplotlib import pyplot as plt

from app.dao.sizes import SizesDAO


router = Router()

@router.message(Command('top'))
async def top(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    if message.chat.id > 0:
        await message.answer('Бот работает только в чате')
        return
    
    msg = 'Топ 10 игроков:\n\n'

    top = await SizesDAO.get_top(chat_id=message.chat.id)
    for key, row in enumerate(top):
        msg += f'{key+1}|{row.name} - {row.size} см.\n'
     
    await message.answer(msg)


@router.message(Command('global_top'))
async def global_top(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    
    msg = 'Топ 10 игроков:\n\n'

    top = await SizesDAO.get_top()
    for key, row in enumerate(top):
        msg += f'{key+1}|{row.name} - {row.size} см.\n'
     
    await message.answer(msg)

@router.message(Command('stats'))
async def stats(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    if message.chat.id > 0:
        await message.answer('Бот работает только в чате')
        return
    
    msg = 'Топ 10 игроков:\n\n'

    top = await SizesDAO.get_top(chat_id=message.chat.id)
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
        plt.close()
     
    await message.answer_photo(types.FSInputFile(filename))

