from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

class Line(Base):
    __tablename__ = 'lines'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    identifier = Column(String)
    owner_id = Column(Integer, ForeignKey("stations.id"))

    station = relationship("Station", back_populates="lines")