from fastapi import WebSocket
from typing import List

# WebSocket manager for tracking and broadcasting to clients
class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []  # List of connected clients

    # Add new client connection
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    # Remove client on disconnect
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # Broadcast message to all connected clients
    async def broadcast_json(self, message):
        for connection in self.active_connections:
            await connection.send_json(message)

# Create single instance of manager to reuse across app
manager = WebSocketManager()
