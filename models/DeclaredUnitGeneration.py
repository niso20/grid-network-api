from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.Base import TimestampMixin

class UnitReading(Base, TimestampMixin):
    __tablename__ = 'declared_unit_generations'

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"))
    mw = Column(Float(precision=53), nullable=True)


    unit = relationship("Unit", back_populates="readings")