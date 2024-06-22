from sqlalchemy import BigInteger, Boolean, Column, Integer, String

from app.database import Base


class Promo(Base):
    # Таблица с промокодами
    __tablename__ = 'promos'

    promo_id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    uses = Column(Integer, nullable=False)

class PromoUsing(Base):
    # Таблица с использованием промокодов
    __tablename__ = 'promos_using'

    promo_id = Column(Integer,primary_key=True, nullable=False)
    user_id = Column(BigInteger, primary_key=True, nullable=False)
    is_used = Column(Boolean, nullable=False)
