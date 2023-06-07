import abc

from aiokafka import AIOKafkaProducer
from redis import Redis


class AbstractCache(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, *args, **kwargs):
        raise NotImplementedError


class RedisCache(AbstractCache):
    def __init__(
            self,
            redis: Redis,
    ):
        self.redis = redis

    async def get_by_id(self, *args, **kwargs):
        data = await self.redis.get(kwargs.get('key'))
        if not data:
            return None

        return data


class AbstractStorage(abc.ABC):
    @abc.abstractmethod
    async def set_data(self, *args, **kwargs):
        raise NotImplementedError


class KafkaStorage(AbstractStorage):
    def __init__(
            self,
            kafka_producer: AIOKafkaProducer
    ):
        self.producer = kafka_producer

    async def set_data(self, *args, **kwargs):
        await self.producer.start()
        try:
            await self.producer.send_and_wait(
                topic=kwargs.get('topic'),
                key=kwargs.get('key'),
                value=kwargs.get('value'),
            )
        except:
            pass


class Storage:
    def __init__(
            self,
            receiver: KafkaStorage,
            sender: RedisCache,
    ):
        self.receiver = receiver
        self.sender = sender

    async def set_data(
            self,
            topic: str,
            key: bytes,
            value: bytes,
    ) -> None:
        """Функция записывает данные в хранидище.

        Args:
            topic (str): Название топика.
            key (bytes): Ключ записи.
            value (bytes): Значение записи.


        """
        await self.receiver.set_data(
            topic=topic,
            key=key,
            value=value,
        )

    async def get_data(
            self,
            key: str,
    ) -> str:
        """Функция получает данные из хранилища по ключу.

        Args:
            key (str): Ключ записи в хранилище.

        Returns:
            str: Значение записи по ключу.


        """
        response = await self.sender.get_by_id(
            key=key,
        )

        return response
