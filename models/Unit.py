from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import TimestampMixin

class Unit(Base, TimestampMixin):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    identifier = Column(String, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"))
    voltage_level = Column(Float(precision=53), nullable=True, default=33)
    inertia = Column(Float(precision=53))
    active = Column(Boolean, default=True)

    station = relationship("Station", back_populates="units")
    readings = relationship("UnitReading", back_populates="unit")