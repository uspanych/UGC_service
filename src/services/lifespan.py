from aiokafka import AIOKafkaProducer
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

from core.config import settings
from db import kafka, mongo, redis


async def startup() -> None:
    redis.redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
    )

    kafka.producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
    )

    mongo.client = AsyncIOMotorClient(
        f'mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}'
    )

    await kafka.producer.start()


async def shutdown() -> None:
    if redis.redis is not None:
        await redis.redis.close()
    if kafka.producer is not None:
        await kafka.producer.stop()