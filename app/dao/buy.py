import logging
from app.basedao import BaseDAO
from app.models.buy import Bought, Payments


class BuyDAO(BaseDAO):
    model = Bought
    uid = Bought.user_id

    @classmethod
    async def use(cls, user_id: int):
        buied = await cls.find_one_or_none(user_id=user_id)
        if buied and buied.using_remain > 0:
            logging.info('Use bought attemption by' + str(user_id))
            await cls.update(user_id, using_remain = buied.using_remain - 1)
            return True
        return False

class PaymentsDAO(BaseDAO):
    model = Payments
    uid = Payments.payload