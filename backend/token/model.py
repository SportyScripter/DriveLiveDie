from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

from pydantic import BaseModel, EmailStr

from db.base_class import Base

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    access_token = Column(String, index=True)
    refresh_token = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.now())

    users = relationship("User", back_populates="tokens")

    class Config:
        orm_mode = True

class AccessTokenRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    access_token: str
    refresh_token: str