from unittest.mock import DEFAULT

from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import TimestampMixin


class Station(Base, TimestampMixin):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    identifier = Column(String, unique=True, index=True)
    voltage_level = Column(Float(precision=53), nullable=True)
    display = Column(Boolean, default=False)
    x = Column(Integer, default=20)
    y = Column(Integer, default=20)
    width = Column(Integer, default=300)
    height = Column(Integer, default=200)
    location = Column(String, nullable=True)
    type = Column(String, nullable=True)
    lines = relationship("Line", back_populates="station")
    units = relationship("Unit", back_populates="station")
    transformers = relationship("Transformer", back_populates="station")