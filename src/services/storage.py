from redis import Redis
import json
import abc
from aiokafka import AIOKafkaProducer


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

        return json.loads(data)


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
    ):
        await self.receiver.set_data(
            topic=topic,
            key=key,
            value=value,
        )

    async def get_data(
            self,
            key: str,
    ):
        response = await self.sender.get_by_id(
            key=key,
        )

        return response
