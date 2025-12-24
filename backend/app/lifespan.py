import asyncio
from contextlib import asynccontextmanager
from app.kafka_consumer import kafka_loop, close_consumer

kafka_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app):
    global kafka_task

    kafka_task = asyncio.create_task(kafka_loop())
    print("✅ Kafka consumer started")

    yield  # app running

    if kafka_task:
        kafka_task.cancel()

    close_consumer()
    print("🛑 Kafka consumer stopped")

