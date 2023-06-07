from kafka import KafkaConsumer
from redis import Redis

from core.config import settings
from models.views import ViewModel


class RedisLoader:
    """Класс закгрузки в редис.

    Класс предназначен для загрузки данных из Kafka в Redis

    """
    def __init__(
            self,
            consumer: KafkaConsumer,
            redis: Redis,
    ) -> None:
        self.consumer = consumer
        self.redis = redis

    def get_kafka_data(self, batch_size: int = 1) -> None:
        """Функция выгрузки из Kafka.

        Функция выгружает данные из кафка в размере <batch_size>.

        Args:
            batch_size (int): Размер пачки данных.

        Returns:
            list: Список с моедлями view.

        """
        batch = []
        for message in self.consumer:
            key, value = message.key, message.value
            batch.append(
                ViewModel(
                    key=key,
                    value=value,
                )
            )
            if len(batch) == batch_size:
                break

        self._set_data_redis(batch)

    def _set_data_redis(self, batch: list[ViewModel]) -> None:

        for item in batch:
            self.redis.set(
                item.key,
                item.value,
                int(settings.TTL_REDIS),
            )
