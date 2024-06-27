import logging
import random
from aiogram import Router, types
from aiogram.filters import Command

from app.dao.promos import PromoUsingDAO
from app.dao.sizes import SizesDAO

router = Router()


variants = [-5,
            -4, -4,
            -3, -3,
            -2, -2,
            -1, -1,
            1, 1, 1, 1, 1,
            2, 2, 2, 2, 2, 2,
            3, 3, 3, 3, 3, 3, 3,
            4, 4, 4, 4, 4, 4, 4, 4,
            5, 5, 5, 5, 5, 5, 5, 5, 
            6, 6, 6, 6, 6, 6, 6, 6,
            7, 7, 7, 7, 7, 7, 7,
            8, 8, 8, 8, 8, 
            9, 9, 9, 9,
            10, 10, 10]

@router.message(Command('dick'))
async def dick(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    if message.chat.id > 0:
        await message.answer('Бот работает только в чате')
        return
    
    row = await SizesDAO.find_one_or_none(chat_id=message.chat.id, user_id=message.from_user.id)
    if row is None:
        logging.debug('New user in chat')
        row = await SizesDAO.add(chat_id=message.chat.id, user_id=message.from_user.id)
    using_promo = await PromoUsingDAO.use(message.from_user.id)
    if using_promo:
        logging.debug("Used promo for user " + str(message.from_user.id) + " chat "+ str(message.chat.id))
    elif row.isUpdated:
        tops = await SizesDAO.find_all(chat_id = message.chat.id)
        number = 1
        for key, top in enumerate(tops):
            if top.user_id != message.from_user.id:
                continue
            number = key + 1
            break
        await message.answer(text=f'<a href="{message.from_user.url}">{message.from_user.first_name}</a>, ты уже играл.\nСейчас он равен {row.size} см.\nТы занимаешь {number} место в топе.\nСледующая попытка завтра.', parse_mode='HTML')
        return
    
    step = random.choice(variants)
    size = row.size + step
    if using_promo:
        await SizesDAO.update(chat_id=message.chat.id, user_id=message.from_user.id, size = size, name = message.from_user.first_name)
    else:
        await SizesDAO.update(chat_id=message.chat.id, user_id=message.from_user.id, size = size, isUpdated = True, name = message.from_user.first_name)

    tops = await SizesDAO.find_all(chat_id = message.chat.id)
    number = 1
    for key, top in enumerate(tops):
        if top.user_id != message.from_user.id:
            continue
        number = key + 1
        break

    if step >= 0:
        await message.answer(text=f'<a href="{message.from_user.url}">{message.from_user.first_name}</a>, твой писюн вырос на {step} см.\nСейчас он равен {size} см.\nТы занимаешь {number} место в топе.\nСледующая попытка завтра!', parse_mode='HTML')
    elif step < 0:
        await message.answer(text=f'<a href="{message.from_user.url}">{message.from_user.first_name}</a>, твой писюн сократился на {step*(-1)} см.\nСейчас он равен {size} см.\n Ты занимаешь {number} место в топе.\nСледующая попытка завтра!', parse_mode='HTML')
