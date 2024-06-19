import logging
from app.daos import SizedDAO


async def reset():
    logging.info('Reset')
    await SizedDAO.reset()