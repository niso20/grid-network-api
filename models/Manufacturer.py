from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import TimestampMixin

class Manufacturer(Base, TimestampMixin):
    __tablename__ = 'manufacturers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    transformers = relationship("Transformer", back_populates="manufacturer")