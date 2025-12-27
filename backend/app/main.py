from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from app.lifespan import lifespan
from app.websocket_manager import live_clients, forecast_clients

app = FastAPI(lifespan=lifespan)


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    live_clients.add(ws)

    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        live_clients.remove(ws)


@app.websocket("/ws/forecast")
async def forecast_websocket_endpoint(ws: WebSocket):
    await ws.accept()
    forecast_clients.add(ws)

    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        forecast_clients.remove(ws)
