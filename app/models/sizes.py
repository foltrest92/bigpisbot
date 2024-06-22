from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String, func

from app.database import Base


class Size(Base):
    # Таблица с размерами
    __tablename__ = 'sizes'

    chat_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, primary_key=True)
    size = Column(Integer, default=0)
    last_update = Column(DateTime, onupdate=func.now(), server_default=func.now())
    isUpdated = Column(Boolean, default=False)
    name = Column(String)
