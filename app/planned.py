from app.daos import SizedDAO


async def reset():
    await SizedDAO.reset()