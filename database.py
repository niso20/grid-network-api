from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosApp.db'
# SQLALCHEMY_DATABASE_URL = 'postgresql://princeak:dRKH5CsZC6Lm4RMggNkjmkr79g25T23u@dpg-d0cacsi4d50c73but2tg-a/powergrid'
# SQLALCHEMY_DATABASE_URL = 'postgresql://princeak@localhost/powerGrid'
SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")
# if SQLALCHEMY_DATABASE_URL is None:
#     SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
