from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import pytest_asyncio
from .settings import test_settings


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def kafka_consumer():
    consumer = AIOKafkaConsumer(
        test_settings.TOPIC,
        bootstrap_servers=test_settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=test_settings.GROUP_ID,
    )
    await consumer.start()
    yield consumer
    await consumer.stop()


@pytest_asyncio.fixture(scope='session')
async def kafka_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=test_settings.KAFKA_BOOTSTRAP_SERVERS,
    )
    await producer.start()
    yield producer
    await producer.stop()
