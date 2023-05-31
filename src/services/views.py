from functools import lru_cache
from redis import Redis
from fastapi import Depends
from db.redis import get_redis
from db.kafka import get_producer
from aiokafka import AIOKafkaProducer
from storage import Storage, RedisCache, KafkaStorage


class ViewsService(Storage):
    pass


@lru_cache()
def get_views_service(
    redis: Redis = Depends(get_redis),
    producer: AIOKafkaProducer = Depends(get_producer),
) -> ViewsService:
    return ViewsService(
        receiver=KafkaStorage(producer),
        sender=RedisCache(redis),
    )
