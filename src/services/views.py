from functools import lru_cache
from redis import Redis
from fastapi import Depends
from db.redis import get_redis
from db.kafka import get_producer
from aiokafka import AIOKafkaProducer
from core.config import settings
from models.views import ViewResponseModel

from .storage import Storage, RedisCache, KafkaStorage


class ViewsService(Storage):
    async def set_data_key(
            self,
            key: bytes,
            value: bytes,
    ) -> None:
        """Метод устанавливает значение кадра фильма по ключу.

        Args:
            key (bytes): Ключ формата <user_uuid+film_uuid>.
            value(bytes): Значение по ключу, кадр фильма.

        """

        await self.set_data(
            key=key,
            value=value,
            topic=settings.TOPIC
        )

    async def get_data_key(
            self,
            key: str,
    ) -> ViewResponseModel:
        """Метод получения записи по ключу.

        Args:
            key (str): Ключ записи в хранилище <user_uuid+film_uuid>

        """

        response = await self.get_data(key)

        return ViewResponseModel(value=response)


@lru_cache()
def get_views_service(
    redis: Redis = Depends(get_redis),
    producer: AIOKafkaProducer = Depends(get_producer),
) -> ViewsService:
    return ViewsService(
        receiver=KafkaStorage(producer),
        sender=RedisCache(redis),
    )
