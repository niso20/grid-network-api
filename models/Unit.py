from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import TimestampMixin

class Line(Base, TimestampMixin):
    __tablename__ = 'lines'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    identifier = Column(String, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"))
    voltage_level = Column(Float(precision=53), nullable=True)
    x = Column(Integer, default=20)
    y = Column(Integer, default=50)

    station = relationship("Station", back_populates="lines")
    readings = relationship("LineReading", back_populates="line")