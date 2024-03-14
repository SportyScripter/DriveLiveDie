from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, DateTime 
from sqlalchemy.orm import relationship
import datetime

from db.base_class import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    hashed_password = Column(String)
    name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_date = Column(DateTime)

    Role_id = Column(Integer, ForeignKey("roles.id"))

    Role = relationship("Role", back_populates="users")
    tokens = relationship("Token", back_populates="users")

    class Config:
        orm_mode = True


class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    access_token = Column(String, index=True)
    refresh_token = Column(String, index=True)
    status = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.now())

    users = relationship("User", back_populates="tokens")

    class Config:
        orm_mode = True

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_date = Column(DateTime, default=datetime.datetime.now())

    users = relationship("User", back_populates="Role")

    class Config:
        orm_mode = True
