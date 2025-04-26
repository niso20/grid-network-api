from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import TimestampMixin

class Connection(Base, TimestampMixin):
    __tablename__ = 'connections'

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True)
    from_station_id = Column(Integer, ForeignKey("stations.id"))
    from_line_id = Column(Integer, ForeignKey("lines.id"))
    from_side = Column(String, default='right')
    to_station_id = Column(Integer, ForeignKey("stations.id"))
    to_line_id = Column(Integer, ForeignKey("lines.id"))
    to_side = Column(String, default='left')
    display = Column(Boolean, default=True)

    fromStation = relationship("Station", foreign_keys=[from_station_id], backref="outgoingConnections")
    toStation = relationship("Station", foreign_keys=[to_station_id], backref="incomingConnections")

    fromLine = relationship("Line", foreign_keys=[from_line_id], backref="outgoingConnections")
    toLine = relationship("Line", foreign_keys=[to_line_id], backref="incomingConnections")