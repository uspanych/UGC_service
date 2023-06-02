from functools import lru_cache
from redis import Redis
from fastapi import Depends
from db.redis import get_redis
from db.kafka import get_producer
from aiokafka import AIOKafkaProducer
from core.config import settings
from .storage import Storage, RedisCache, KafkaStorage


class ViewsService(Storage):
    async def set_data_key(
            self,
            key: bytes,
            value: bytes,
    ) -> None:

        await self.set_data(
            key=key,
            value=value,
            topic=settings.TOPIC
        )


@lru_cache()
def get_views_service(
    redis: Redis = Depends(get_redis),
    producer: AIOKafkaProducer = Depends(get_producer),
) -> ViewsService:
    return ViewsService(
        receiver=KafkaStorage(producer),
        sender=RedisCache(redis),
    )
