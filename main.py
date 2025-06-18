from fastapi import FastAPI, WebSocket
from WebSocketManager import WebSocketManager
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
from database import engine
import models

# Routes
import time
import os
import logging
from routers import auth
from routers import stations
from routers import lines
from routers import units
from routers import connections
from routers import transformers
from routers import manufacturers
from routers import frequency

from services.MqttService import start_mqtt, mqttTranscoQueue, mqttGencoQueue
from runSQLScript import runScripts
from seeders.BaseSeeder import runSeeders

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create separate managers for different data types
stationManager = WebSocketManager()
gencoManager = WebSocketManager()

# Define the lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # print(os.environ.get("SQLALCHEMY_DATABASE_URL"))
    try:
        await runSeeders()
        runScripts()
    except Exception as e:
        logger.error(f"Error durring database setup: {e}")
        print((f"Error durring database setup: {e}"))

    loop = asyncio.get_running_loop()

    mqttTask = None

    # Start MQTT listener
    # start_mqtt(loop)
    try:
        mqttTask = asyncio.create_task(start_mqtt_with_retry(loop, 10))
        print("MQTT connection task started")
    except Exception as e:
        logger.error(f"Failed to start MQTT task: {e}")

    # Start background task to process and forward messages
    task = asyncio.create_task(process_mqtt_data())

    # Yield control to FastAPI until shutdown
    yield

    # Cleanup on shutdown (optional)
    if mqttTask:
        mqttTask.cancel()
    task.cancel()

app = FastAPI(lifespan=lifespan)

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
app.include_router(units.router)
app.include_router(connections.router)
app.include_router(transformers.router)
app.include_router(manufacturers.router)
app.include_router(auth.router)
app.include_router(frequency.router)

# Run this when FastAPI starts
# @app.on_event("startup")
# async def startup_event():
#     loop = asyncio.get_event_loop()  # Get running asyncio event loop
#     start_mqtt()  # Start MQTT client
#     loop.create_task(process_mqtt_data())  # Launch background task for processing messages

async def start_mqtt_with_retry(loop, max_retries=5, retry_delay=10):
    """Start MQTT with retry logic - won't crash the app if it fails"""
    retry_count = 0

    while retry_count < max_retries:
        try:
            logger.info(f"Attempting MQTT connection (attempt {retry_count + 1}/{max_retries})")
            start_mqtt(loop)
            logger.info("MQTT connected successfully")
            return
        except Exception as e:
            retry_count += 1
            logger.error(f"MQTT connection failed (attempt {retry_count}/{max_retries}): {e}")

            if retry_count < max_retries:
                logger.info(f"Retrying MQTT connection in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("Max MQTT connection retries reached. Application will continue without MQTT.")
                return

# Async task to consume MQTT messages, save to DB, and broadcast via WebSocket
async def process_mqtt_data():
    while True:
        transcoData = await mqttTranscoQueue.get()             # Wait for next data from queue
        gencoData = await mqttGencoQueue.get()
        # print(data)
        # await save_station_data(data)             # Save to PostgreSQL
        await stationManager.broadcast_json(transcoData)        # Broadcast to all connected WebSocket clients

# WebSocket endpoint for clients to connect and receive updates
@app.websocket("/ws/station")
async def websocket_endpoint(websocket: WebSocket):
    await stationManager.connect(websocket)  # Add new client
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except Exception:
        stationManager.disconnect(websocket)  # Remove client on disconnect

@app.websocket("/ws/genco")
async def websocket_endpoint(websocket: WebSocket):
    await gencoManager.connect(websocket)  # Add new client
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except Exception:
        gencoManager.disconnect(websocket)  # Remove client on disconnect