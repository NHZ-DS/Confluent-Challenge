# Real-Time Pollution Streaming Backend

This backend consumes real-time pollution data from a Kafka topic
and streams it to connected clients using WebSockets.

## Tech Stack
- FastAPI
- Kafka (Confluent)
- WebSockets
- asyncio

## Run Locally
```bash
uvicorn app.main:app --reload

