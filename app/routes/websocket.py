from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import asyncio

router = APIRouter()

# =========================
# ACTIVE CLIENT MANAGER
# =========================
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))

    async def broadcast(self, data: dict):
        dead = []

        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(data))
            except Exception:
                dead.append(connection)

        for d in dead:
            self.disconnect(d)


manager = ConnectionManager()

# =========================
# WEBSOCKET ENDPOINT
# =========================
@router.websocket("/analytics")
async def analytics_socket(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            # heartbeat ping
            await asyncio.sleep(10)
            await websocket.send_text(json.dumps({"type": "ping"}))

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception:
        manager.disconnect(websocket)


# =========================
# EXTERNAL BROADCAST FUNCTION
# =========================
async def broadcast_analytics(data: dict):
    await manager.broadcast(data)