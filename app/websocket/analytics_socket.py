from fastapi import APIRouter, WebSocket
import json
import asyncio

router = APIRouter()

clients = []

# =========================
# CONNECT SOCKET
# =========================
@router.websocket("/analytics")
async def analytics_socket(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            # keep connection alive
            await asyncio.sleep(5)

    except:
        clients.remove(websocket)


# =========================
# BROADCAST FUNCTION
# =========================
async def broadcast_analytics(data: dict):
    dead_clients = []

    for client in clients:
        try:
            await client.send_text(json.dumps(data))
        except:
            dead_clients.append(client)

    for d in dead_clients:
        clients.remove(d)