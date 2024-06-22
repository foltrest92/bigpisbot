import logging

from sqlalchemy import and_, desc, select, update

from app.dao.base import BaseDAO
from app.models import Size
from app.database import async_session_maker


class SizesDAO(BaseDAO):
    model = Size

    @classmethod
    async def find_all(cls, **filter_by):
        logging.debug('SizedDAO: find all: filter_by' + str(filter_by))
        async with async_session_maker() as session:
            query = select(Size.__table__.columns).filter_by(**filter_by).order_by(desc(Size.size))
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def update(cls, chat_id: int, user_id, **data):
        logging.debug('SizedDAO: update: chat_id:'+str(chat_id)+' user_id: '+str(user_id)+' data: '+ str(data))
        async with async_session_maker() as session:
            query = update(Size).where(and_(Size.chat_id == chat_id, Size.user_id == user_id)).values(**data).returning(Size)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()
            # return result
    
    @classmethod
    async def get_top(cls, chat_id: int = None, limit: int = 10):
        logging.debug('SizedDAO: get_top: chat_id:'+str(chat_id)+' limit: ' + str(limit))
        async with async_session_maker() as session:
            if chat_id:
                query = select(Size.__table__.columns).filter_by(chat_id=chat_id).order_by(desc(Size.size)).limit(10)
            else:
                query = select(Size.__table__.columns).order_by(desc(Size.size)).limit(10)
            result = await session.execute(query)
            return result.mappings().all()
    
    @classmethod
    async def reset(cls):
        logging.debug('SizedDAO: RESET')
        async with async_session_maker() as session:
            query = update(Size).values(isUpdated=False)
            await session.execute(query)
            await session.commit()
