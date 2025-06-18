from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.Base import TimestampMixin

class UnitReading(Base, TimestampMixin):
    __tablename__ = 'declared_generation'

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"))
    v = Column(Float(precision=53), nullable=True)
    a = Column(Float(precision=53), nullable=True)
    mw = Column(Float(precision=53), nullable=True)
    mx = Column(Float(precision=53), nullable=True)
    f = Column(Float(precision=53), nullable=True)
    pf = Column(Float(precision=53), nullable=True)
    t = Column(DateTime, nullable=True, index=True)

    unit = relationship("Unit", back_populates="readings")