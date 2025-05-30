from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosApp.db'
SQLALCHEMY_DATABASE_URL = 'postgresql://princeak:dRKH5CsZC6Lm4RMggNkjmkr79g25T23u@dpg-d0cacsi4d50c73but2tg-a/powergrid'
# SQLALCHEMY_DATABASE_URL = 'postgresql://princeak@localhost/powerGrid'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
