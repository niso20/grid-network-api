from fastapi import FastAPI

import database
from database import engine
import models

app = FastAPI()

models.init_models(engine)