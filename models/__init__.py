# models/__init__.py
from models.Line import Line
from models.Unit import Unit
from models.Station import Station
from models.Connection import Connection
from models.LineReading import LineReading
from models.UnitReading import UnitReading
from models.Manufacturer import Manufacturer
from models.Transformer import Transformer
from models.Role import Role
from models.User import User
from models.Frequency import Frequency

# Add any more models here as you create them

def init_models(engine):
    from database import Base
    Base.metadata.create_all(bind=engine)