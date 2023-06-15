from functools import lru_cache
from statistics import mean

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from db.mongo import get_client
from models.mongo import FilmResponseModel, LikesModel, FilmAvgModel
from .storage import MongoStorage


class LikesService(MongoStorage):
    """Класс предоставляет возможность редактировать-читать лайки"""

    async def get_data_by_film(
            self,
            query: dict,
    ) -> FilmResponseModel:
        """Метод выполняет поиск в базе по query.

        Args:
            query (dict): Параметры поиска данных.

        Returns:
            dict: Найденный документ.


        """

        result = await self.get_data_many(
            query=query,
            collection='likes',
        )

        positive_vote_count = len([document for document in result if document.get('point') >= 5])
        negative_vote_count = len([document for document in result if document.get('point') < 5])

        return FilmResponseModel(
            film_id=query.get('film_id'),
            positive_vote=positive_vote_count,
            negative_vote=negative_vote_count,
        )

    async def get_avg_likes(
            self,
            query: dict,
    ) -> FilmAvgModel:
        """Метод возвращает среднюю оценку по фильму.

        Args:
            query (dict): Параметр для поиска данных.


        """

        result = await self.get_data_many(
            query=query,
            collection='likes',
        )

        point_avg = []
        for document in result:
            point_avg.append(document.get('point'))

        avg_value = mean(point_avg)

        return FilmAvgModel(
            film_id=query.get('film_id'),
            avg_vote=avg_value
        )

    async def update_data_by_document(
            self,
            document: LikesModel
    ):
        """Метод получает документ на вход и сохраняет его в базе.

        Args:
            document (dict): Структура документа для хранения в базе.


        """

        await self.update_data(
            document={
                'filter_key': 'film_id',
                'filter_value': document.film_id,
                'updated_key': 'point',
                'updated_value': document.point,
            },
            collection='likes',
        )

    async def set_data_by_document(
            self,
            document: LikesModel,
    ) -> None:
        """Метод получает документ на вход и сохраняет его в базе.

        Args:
            document (dict): Структура документа для хранения в базе.


        """

        await self.set_data(
            document=document,
            collection='likes',
        )

    async def delete_data_by_document(
            self,
            query: dict,
    ) -> None:
        """Метод удаляет документ по запросу.

        Args:
            query (dict): Ключ удаления записи.


        """

        await self.delete_data(
            query=query,
            collection='likes',
        )


@lru_cache()
def get_likes_service(
    client: AsyncIOMotorClient = Depends(get_client),
) -> LikesService:
    return LikesService(
        client=client,
    )
