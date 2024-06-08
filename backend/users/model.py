from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime

from db.base_class import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    hashed_password = Column(String)
    first_name = Column(String, index=True, nullable=True)
    last_name = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_date = Column(DateTime, default=datetime.datetime.now())
    role = Column(String, default="user")

    tokens = relationship("Token", back_populates="users")

    class Config:
        orm_mode = True
