from sqlalchemy import Boolean, Column, Integer, DateTime, String, func, BigInteger, ForeignKey
from app.database import Base


class Size(Base):
    __tablename__ = 'sizes'

    chat_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, primary_key=True)
    size = Column(Integer, default=0)
    last_update = Column(DateTime, onupdate=func.now(), server_default=func.now())
    isUpdated = Column(Boolean, default=False)
    name = Column(String)

class Promo(Base):
    __tablename__ = 'promos'

    promo_id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    uses = Column(Integer, nullable=False)

class PromoUsing(Base):
    __tablename__ = 'promos_using'

    promo_id = Column(Integer,primary_key=True, nullable=False)
    user_id = Column(BigInteger, primary_key=True, nullable=False)
    is_used = Column(Boolean, nullable=False)
