from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship


class Station(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    identifier = Column(String)
    display = Column(Boolean, default=True)
    lines = relationship("Line", back_populates="station")