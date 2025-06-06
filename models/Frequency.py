from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import TimestampMixin

class Frequency(Base, TimestampMixin):
    __tablename__ = 'frequencies'

    id = Column(Integer, primary_key=True, index=True)
    f = Column(Float)
    t = Column(String)
    df = Column(Float, nullable=True)
    dt = Column(Float, nullable=True)
    rocof = Column(Float, nullable=True)