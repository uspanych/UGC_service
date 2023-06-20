from functools import lru_cache
from typing import List

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from db.mongo import get_client
from models.mongo import ReviewModel
from .storage import MongoStorage


class ReviewService(MongoStorage):
    """Класс предоставляет возможность управлять рецензиями."""

    async def get_reviews_by_query(
            self,
            query: str | dict,
    ) -> List[ReviewModel]:
        """Метод возвращает список рецензий по фильтру.

        Args:
            query (dict): Параметры поиска данных.

        Returns:
            list: Найденный документ.


        """

        reviews_list = await self.get_data_many(
            query=query,
            collection='reviews',
        )

        return [
            ReviewModel(
                review_id=document.get('review_id'),
                user_id=document.get('user_id'),
                film_id=document.get('film_id'),
                review=document.get('review'),
                date=document.get('date'),
                like=document.get('like')
            ) for document in reviews_list
        ]

    async def set_data_by_document(
            self,
            document: ReviewModel,
    ) -> None:
        """Метод получает документ на вход и сохраняет его в базе.

        Args:
            document (dict): Параметр для поиска данных.


        """

        await self.set_data(
            document=document,
            collection='reviews'
        )

    async def update_data_document(
            self,
            document: ReviewModel,
    ):
        """Метод позволяет добавить лайк к рецензии.

        Args:
            document (dict): Структура документа для обновления.


        """

        await self.update_data(
            document={
                'filter_key': 'review_id',
                'filter_value': document.review_id,
                'updated_key': 'like',
                'updated_value': document.like
            },
            collection='reviews'
        )


@lru_cache()
def get_reviews_service(
        client: AsyncIOMotorClient = Depends(get_client),
) -> ReviewService:
    return ReviewService(
        client=client,
    )
