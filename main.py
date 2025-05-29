from fastapi import FastAPI, WebSocket
from WebSocketManager import manager
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
import database
from database import engine
import models
from routers import stations
from routers import lines
from routers import connections
from routers import transformers
from routers import manufacturers
from services.MqttService import start_mqtt, mqtt_queue
from runSQLScript import runScripts

# Define the lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    runScripts()

    loop = asyncio.get_running_loop()
    # Start MQTT listener
    start_mqtt(loop)

    # Start background task to process and forward messages
    task = asyncio.create_task(process_mqtt_data())

    # Yield control to FastAPI until shutdown
    yield

    # Cleanup on shutdown (optional)
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
app.include_router(connections.router)
app.include_router(transformers.router)
app.include_router(manufacturers.router)

# Run this when FastAPI starts
# @app.on_event("startup")
# async def startup_event():
#     loop = asyncio.get_event_loop()  # Get running asyncio event loop
#     start_mqtt()  # Start MQTT client
#     loop.create_task(process_mqtt_data())  # Launch background task for processing messages

# Async task to consume MQTT messages, save to DB, and broadcast via WebSocket
async def process_mqtt_data():
    while True:
        data = await mqtt_queue.get()             # Wait for next data from queue
        # print(data)
        # await save_station_data(data)             # Save to PostgreSQL
        await manager.broadcast_json(data)        # Broadcast to all connected WebSocket clients

# WebSocket endpoint for clients to connect and receive updates
@app.websocket("/ws/data")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)  # Add new client
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except Exception:
        manager.disconnect(websocket)  # Remove client on disconnect