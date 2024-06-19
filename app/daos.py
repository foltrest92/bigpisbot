import logging
from sqlite3 import IntegrityError
from sqlalchemy import desc, insert, select, update, and_
from app.dao.base import BaseDAO
from app.models import Promo, PromoUsing, Size
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
    async def use(cls, code: str, user_id: int) -> bool:
        logging.debug('Using promocode '+ str(code))
        promo =  await cls.find_one_or_none(code=code)
        if promo and promo.uses>0:
            async with async_session_maker() as session:
                try:
                    adding_using_promo_query = insert(PromoUsing).values(
                        promo_id = promo.promo_id,
                        user_id = user_id,
                        is_used = False
                    )
                    await session.execute(adding_using_promo_query)
                except:
                    logging.debug('Promocode already used. Promo_id: '+ str(promo.promo_id) + ', User_id: '+ str(user_id))
                    return False   
                edit_promo_query = update(Promo).where(Promo.code == code).values(uses=promo.uses-1)
                await session.execute(edit_promo_query)
                await session.commit()
                logging.debug('Promocode '+ str(code) + ' used, remains: '+ str(promo.uses-1))
            return True
        logging.debug('Promocode didnt use')
        return False
    
class PromoUsingDAO(BaseDAO):
    model = PromoUsing

    @classmethod
    async def use(cls, user_id: int) -> bool:
        logging.debug("Check promocode for user "+ str(user_id))
        async with async_session_maker() as session:
            not_used_promos = await cls.find_all(user_id = user_id, is_used = False)
            if not_used_promos:
                logging.debug('Using promo for chat')
                use_promo = update(PromoUsing).where(and_(PromoUsing.user_id==user_id, PromoUsing.promo_id == not_used_promos[0].promo_id)).values(is_used=True)
                await session.execute(use_promo)
                await session.commit()
                return True
        logging.debug("No not used promos")
        return False