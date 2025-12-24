from fastapi import WebSocket

clients: set[WebSocket] = set()


async def broadcast(message: str):
    dead_clients = []

    for ws in clients:
        try:
            await ws.send_text(message)
        except Exception:
            dead_clients.append(ws)

    for ws in dead_clients:
        clients.remove(ws)

