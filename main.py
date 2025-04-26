from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database
from database import engine
import models
from routers import stations
from routers import lines
from routers import connections

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.init_models(engine)

app.include_router(stations.router)
app.include_router(lines.router)
app.include_router(connections.router)