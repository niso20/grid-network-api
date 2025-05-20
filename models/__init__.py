# models/__init__.py
from models.Line import Line
from models.Station import Station
from models.Connection import Connection
from models.LineReading import LineReading
from models.Manufacturer import Manufacturer
from models.Transformer import Transformer

# Add any more models here as you create them

def init_models(engine):
    from database import Base
    Base.metadata.create_all(bind=engine)