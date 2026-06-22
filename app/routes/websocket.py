from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


# =========================
# CONNECTION MANAGER (ENTERPRISE VERSION)
# =========================
class ConnectionManager:
    def __init__(self):
        # user_email -> [websockets]
        self.active_connections: dict[str, list] = {}

    async def connect(self, websocket: WebSocket, user_id: str = "anonymous"):
        await websocket.accept()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = []

        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket):
        for user_id, sockets in self.active_connections.items():
            if websocket in sockets:
                sockets.remove(websocket)

                if not sockets:
                    del self.active_connections[user_id]
                break

    async def send_to_user(self, user_id: str, message: dict):
        sockets = self.active_connections.get(user_id, [])
        for conn in sockets:
            await conn.send_json(message)

    async def broadcast(self, message: dict):
        for sockets in self.active_connections.values():
            for conn in sockets:
                await conn.send_json(message)


manager = ConnectionManager()


# =========================
# LIVE DASHBOARD SOCKET
# =========================
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    # optional query param: ?user=email
    user_id = websocket.query_params.get("user", "anonymous")

    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()

            # echo back OR dashboard updates
            await manager.send_to_user(user_id, {
                "event": "message",
                "data": data
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)