# models/__init__.py
from models.Line import Line
from models.Station import Station

# Add any more models here as you create them

def init_models(engine):
    from database import Base
    Base.metadata.create_all(bind=engine)