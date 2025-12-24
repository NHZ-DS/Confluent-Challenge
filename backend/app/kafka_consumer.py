import asyncio
from confluent_kafka import Consumer
from get_config import read_config
from app.websocket_manager import broadcast

# ---- Kafka configuration ----
config = read_config()

consumer = Consumer(config)
consumer.subscribe(["pollution"])


async def kafka_loop():
    """
    Poll Kafka continuously,
    but send at most ONE message every 2 seconds.
    """
    latest_payload = None

    while True:
        msg = consumer.poll(0.1)
        if msg and not msg.error():
            latest_payload = msg.value().decode()

        if latest_payload:
            await broadcast(latest_payload)
            latest_payload = None

            # ⏱️ throttle output
            await asyncio.sleep(2)
        else:
            await asyncio.sleep(0.1)


def close_consumer():
    consumer.close()

