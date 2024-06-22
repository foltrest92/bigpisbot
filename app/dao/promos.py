import logging

from sqlalchemy import and_, insert, update

from app.dao.base import BaseDAO
from app.models import Promo, PromoUsing
from app.database import async_session_maker


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
    
    @classmethod
    async def update(cls, code: str, uses: int):
        logging.info('Update promo'+code)
        async with async_session_maker() as session:
            query = update(Promo).where(Promo.code == code).values(uses=uses)
            await session.execute(query)
            await session.commit()
            logging.debug('Promocode updated')

    
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