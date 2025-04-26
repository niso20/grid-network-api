from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.Base import TimestampMixin

class LineReading(Base, TimestampMixin):
    __tablename__ = 'line_readings'

    id = Column(Integer, primary_key=True, index=True)
    line_id = Column(Integer, ForeignKey("lines.id"))
    v = Column(Float(precision=53), nullable=True)
    a = Column(Float(precision=53), nullable=True)
    mw = Column(Float(precision=53), nullable=True)
    mx = Column(Float(precision=53), nullable=True)
    f = Column(Float(precision=53), nullable=True)
    pf = Column(Float(precision=53), nullable=True)
    t = Column(DateTime, nullable=True, index=True)

    line = relationship("Line", back_populates="readings")