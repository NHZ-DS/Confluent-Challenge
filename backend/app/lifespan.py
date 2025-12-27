import asyncio
from contextlib import asynccontextmanager
from app.kafka_consumer import kafka_loop, close_consumer,forecast_loop

kafka_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app):
    global kafka_task

    kafka_task = asyncio.create_task(kafka_loop())
    forecast_task = asyncio.create_task(forecast_loop())

    print("✅ Kafka consumer started")

    yield  # app running

    if kafka_task:
        kafka_task.cancel()

    close_consumer()
    print("🛑 Kafka consumer stopped")

import asyncio
from contextlib import asynccontextmanager
from app.kafka_consumer import kafka_loop, close_consumer,forecast_loop

kafka_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app):
    global kafka_task

    kafka_task = asyncio.create_task(kafka_loop())
    forecast_task = asyncio.create_task(forecast_loop())

    print("✅ Kafka consumer started")

    yield  # app running

    if kafka_task:
        kafka_task.cancel()

    close_consumer()
    print("🛑 Kafka consumer stopped")

