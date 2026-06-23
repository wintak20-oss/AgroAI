from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

router = APIRouter()

active_connections = []


# =========================
# CONNECT ADMIN DASHBOARD
# =========================
@router.websocket("/ws/admin")
async def admin_dashboard_ws(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            # keep alive
            await websocket.receive_text()

    except WebSocketDisconnect:
        active_connections.remove(websocket)


# =========================
# BROADCAST REAL-TIME DATA
# =========================
async def broadcast_admin_update(data: dict):
    dead = []

    for conn in active_connections:
        try:
            await conn.send_text(json.dumps(data))
        except:
            dead.append(conn)

    for d in dead:
        active_connections.remove(d)