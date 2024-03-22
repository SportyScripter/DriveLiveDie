from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base

class Vehicle(Base):
    __tablename__="vehicles"
    id = Column(Integer, primary_key = True, index = True, autoincrement =True)
    user_id = Column(Integer, ForeignKey("users.id"))
    make = Column(String)
    make_id = Column(Integer)
    year = Column(Integer)
    model = Column(String)
    make_model_id = Column(Integer)
    trim_id = Column(Integer)
    trim_name = Column(String)
    trim_description = Column(String)
    msrp = Column(Integer)
    invoice = Column(Integer)
    interior = Column(String)
    rgb = Column(String)
    


    users = relationship("User", back_populates="vehicles")
