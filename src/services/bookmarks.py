from functools import lru_cache
from typing import List

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from db.mongo import get_client
from models.mongo import BookmarksModel
from .storage import MongoStorage


class BookmarksService(MongoStorage):

    async def get_data_by_user(
            self,
            query: dict,
    ) -> List[BookmarksModel]:
        """Метод выполняет поиск закладок пользователя.

        Args:
            query (dict): Параметр поиска данных.

        Returns:
            dict: Найденный документ.


        """

        result = await self.get_data_many(
            query=query,
            collection='bookmarks',
        )

        return [
            BookmarksModel(
                user_id=document.get('user_id'),
                film_id=document.get('film_id'),
            ) for document in result
        ]

    async def set_data_by_user(
            self,
            document: BookmarksModel,
    ) -> None:
        """Метод получает документ на вход и сохраняет его в базе.

        Args:
            document (dict): Параметр для поиска данных.


        """

        await self.set_data(
            document=document,
            collection='bookmarks',
        )

    async def delete_document(
            self,
            query: dict,
    ) -> None:
        """Метод удаляет документ по запросу.

        Args:
            query (dict): Ключ удаления записи.


        """

        await self.delete_data(
            query=query,
            collection='bookmarks',
        )


@lru_cache()
def get_bookmarks_service(
        client: AsyncIOMotorClient = Depends(get_client),
) -> BookmarksService:
    return BookmarksService(
        client=client,
    )
