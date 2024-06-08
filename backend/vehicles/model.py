from sqlalchemy import Column, Integer, String, DateTime
import datetime

from db.base_class import Base

class Token(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    marka = Column(String)
    model = Column(String)
    color = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now())

    class Config:
        orm_mode = True
