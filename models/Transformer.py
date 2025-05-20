from unittest.mock import DEFAULT

from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import TimestampMixin


class Transformer(Base, TimestampMixin):
    __tablename__ = 'transformers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"), index=True)
    serial_no = Column(String, nullable=True)
    power_rating = Column(Integer, default=False)
    power_rating_unit = Column(String)
    type_of_cooling = Column(String, nullable=True)
    voltage_rating = Column(String)
    manufacture_year = Column(Integer, nullable=True, index=True)
    installation_year = Column(Integer, nullable=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=True, index=True)
    station = relationship("Station", back_populates="transformers")
    manufacturer = relationship("Manufacturer", back_populates="transformers")