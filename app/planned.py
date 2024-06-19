from datetime import datetime
import logging
import os
from app.daos import SizedDAO


async def reset():
    logging.info('Reset')
    await SizedDAO.reset()

async def clean_figs():
    logging.info('Clean figs')
    num = 0
    now_hour = datetime.now().hour
    for filename in os.listdir('figs'):
        if filename[-8:-6].isdigit() and ( now_hour > int(filename[-8:-6])):
            os.remove('figs/'+filename)
            num += 1
    logging.info('Deleted '+str(num)+' figs')
        