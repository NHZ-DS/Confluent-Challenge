from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from app.lifespan import lifespan
from app.websocket_manager import clients

app = FastAPI(lifespan=lifespan)


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)

    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        clients.remove(ws)

