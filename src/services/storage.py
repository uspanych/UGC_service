import abc

from aiokafka import AIOKafkaProducer
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from models.mongo import LikesModel
from redis import Redis
from typing import Type


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
        try:
            await self.producer.send_and_wait(
                topic=kwargs.get('topic'),
                key=kwargs.get('key'),
                value=kwargs.get('value'),
            )
        except:
            pass


class MongoStorage(AbstractStorage):
    def __init__(
        self,
        client: AsyncIOMotorClient,
    ):
        self.client = client

    async def get_data_one(
        self,
        query: dict,
        collection: str,
    ) -> dict:
        """Метод выполняет поиск в базе по query.

        Args:
            query (dict): Параметры поиска данных.
            collection (str): Название коллекции для поиска.

        Returns:
            dict: Найденный документ.


        """

        db = self.client.films
        result = await db[collection].find_one(
            {
                query.get('key'): query.get('value')
            }
        )

        return result

    async def get_data_many(
        self,
        query: dict | str,
        collection: str,
    ) -> list:
        """Метод выполняет поиск в базе по query.

        Args:
            query (dict): Параметры поиска данных.
            collection (str): Название коллекции для поиска.

        Returns:
            dict: Найденный документ.


        """

        db = self.client.films
        result = db[collection].find(query)

        documents_list = []
        async for document in result:
            documents_list.append(document)

        return documents_list

    async def set_data(
            self,
            document: BaseModel,
            collection: str,
    ) -> None:
        """Метод получает документ на вход и сохраняет его в базе.

        Args:
            document (dict): Набор ключей для поиска данных.
            collection (str): Название коллекции для поиска.


        """

        db = self.client.films
        await db[collection].insert_one(document.dict())

    async def update_data(
            self,
            document: dict,
            collection: str,
    ) -> None:
        """Метод обновляет данные по полученному документу.

        Args:
            document (dict): Набор ключей для поиска данных.
            collection (str): Название коллекции для поиска.


        """

        db = self.client.films
        await db[collection].update_one(
            {
                document.get('filter_key'): document.get('filter_value')
            },
            {
                '$set': {
                    document.get('updated_key'): document.get('updated_value')
                }
            }
        )

    async def delete_data(
            self,
            query: dict,
            collection: str,
    ):
        """Метод обновляет данные по полученному документу.

        Args:
            query (str): Параметры поиска данных.
            collection (str): Название коллекции для поиска.


        """

        db = self.client.films
        await db[collection].delete_one(query)


class Storage:
    def __init__(
            self,
            receiver: KafkaStorage = None,
            sender: RedisCache = None,
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
