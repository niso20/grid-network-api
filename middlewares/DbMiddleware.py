from fastapi import Depends
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import  Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DB = Annotated[Session, Depends(get_db)]