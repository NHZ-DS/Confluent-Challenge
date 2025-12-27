import asyncio
import time, random, json
from confluent_kafka import Consumer
from get_config import read_config
from app.websocket_manager import broadcast_live, broadcast_forecast

# ---- Kafka configuration ----
base_config = read_config()

live_config = base_config.copy()
live_config["group.id"] = "live-consumer-group"
# live_config.setdefault("auto.offset.reset", "latest")

forecast_config = base_config.copy()
forecast_config["group.id"] = "forecast-consumer-group"
# forecast_config.setdefault("auto.offset.reset", "latest")

live_consumer = Consumer(live_config)
forecast_consumer = Consumer(forecast_config)

live_consumer.subscribe(["pollution"])
forecast_consumer.subscribe(["pollution"])

async def kafka_loop():
    """
    Poll Kafka continuously,
    but send at most ONE message every 2 seconds.
    """
    latest_payload = None

    while True:
        msg = live_consumer.poll(0.1)
        if msg and not msg.error():
            latest_payload = msg.value().decode()

        if latest_payload:
            await broadcast_live(latest_payload)
            latest_payload = None
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(0.1)


async def forecast_loop():
    """
    Poll Kafka continuously,
    but send at most ONE message every 20 seconds.
    """
    latest_payload = None

    while True:
        msg = forecast_consumer.poll(0.1)
        if msg and not msg.error():
            latest_payload = msg.value().decode()

        if latest_payload:
            await broadcast_forecast(latest_payload)
            latest_payload = None
            await asyncio.sleep(20)
        else:
            await asyncio.sleep(0.1)


def close_consumer():
    live_consumer.close()
    forecast_consumer.close()
