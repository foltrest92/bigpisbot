from sqlalchemy import Boolean, Column, Integer, DateTime, String, func, BigInteger
from app.database import Base


class Size(Base):
    __tablename__ = 'sizes'

    chat_id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, primary_key=True)
    size = Column(Integer, default=0)
    last_update = Column(DateTime, onupdate=func.now(), server_default=func.now())
    isUpdated = Column(Boolean, default=False)
    name = Column(String)