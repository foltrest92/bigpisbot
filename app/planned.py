import asyncio
import logging
import os
from datetime import datetime

from app.dao.sizes import SizesDAO


async def reset():
    # Ежедневный сброс счетчика роста
    while True:
        logging.info("Trying to reset")
        try:
            logging.info('Reset')
            await SizesDAO.reset()
        except Exception as e:
            logging.error(e)
            logging.error("Unable to reset. Waiting 60 secounds...")
            await asyncio.sleep(60)
            continue
        else:
            logging.info('Resetted')
            break

async def clean_figs():
    # Очистка папки с картинками статистики. Не удаляется за текущий час.
    logging.info('Clean figs')
    num = 0
    now_hour = datetime.now().hour
    for filename in os.listdir('figs'):
        if filename[-8:-6].isdigit() and ( now_hour > int(filename[-8:-6])):
            os.remove('figs/'+filename)
            num += 1
    logging.info('Deleted '+str(num)+' figs')
        