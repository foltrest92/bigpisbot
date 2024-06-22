from datetime import datetime
import logging
import os
from app.daos import SizedDAO
import asyncio


async def reset():
    while True:
        logging.info("Trying to reset")
        try:
            logging.info('Reset')
            await SizedDAO.reset()
        except Exception as e:
            logging.error(e)
            logging.error("Unable to reset. Waiting 60 secounds...")
            await asyncio.sleep(60)
            continue
        else:
            logging.info('Resetted')
            break

async def clean_figs():
    logging.info('Clean figs')
    num = 0
    now_hour = datetime.now().hour
    for filename in os.listdir('figs'):
        if filename[-8:-6].isdigit() and ( now_hour > int(filename[-8:-6])):
            os.remove('figs/'+filename)
            num += 1
    logging.info('Deleted '+str(num)+' figs')
        