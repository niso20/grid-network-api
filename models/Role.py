from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    surname = Column(String, nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"))

    station = relationship("Station", back_populates="lines")