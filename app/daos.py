import logging
from sqlalchemy import desc, select, update, and_
from app.dao.base import BaseDAO
from app.models import Promo, Size
from app.database import async_session_maker

class SizedDAO(BaseDAO):
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

class PromoDAO(BaseDAO):
    model = Promo
    uid = Promo.promo_id

    @classmethod
    async def use(cls, code: str) -> bool:
        logging.debug('Using promocode '+ code)
        promo =  await cls.find_one_or_none(code=code)
        if promo and promo.uses>0:
            async with async_session_maker() as session:
                query = update(Promo).where(Promo.code == code).values(uses=promo.uses-1)
                await session.execute(query)
                await session.commit()
                logging.debug('Promocode '+ str(code) + ' used, remains: '+ str(promo.uses-1))
            return True
        logging.debug('Promocode didnt use')
        return False
    