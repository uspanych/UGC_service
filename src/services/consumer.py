from aiokafka import AIOKafkaConsumer
from redis import Redis
from db.redis import get_redis


class Consumer:
    def __init__(
            self,
            redis: Redis,
            consumer: AIOKafkaConsumer,
    ):
        self.redis = redis
        self.consumer = consumer

    async def start_consumer(
            self,

    ):