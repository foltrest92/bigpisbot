from sqlalchemy import Column, Integer, BigInteger, String, SmallInteger
from app.database import Base


class Bought(Base):
    __tablename__ = 'bought'

    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    using_remain = Column(Integer, nullable=False)

class Payments(Base):
    __tablename__ = 'payments'

    user_id = Column(BigInteger, nullable=False)
    payload = Column(String, nullable=False, primary_key=True)
    price = Column(Integer, nullable=False)
    status = Column(SmallInteger, nullable=False, default=1)
    product = Column(Integer, nullable=False)