from fastapi import APIRouter, Body, Depends
from services.review import ReviewService, get_reviews_service
from models.mongo import ReviewModel
from typing import List, Optional
from http import HTTPStatus
from fastapi.logger import logger

router = APIRouter()


@router.get(
    '/reviews',
    description='Метод возвращает список рецензий',
)
async def get_review(
        key: Optional[str] = None,
        value: Optional[str] = None,
        review_service: ReviewService = Depends(get_reviews_service),
) -> List[ReviewModel]:

    query: str | dict = {key: value}

    if key or value is None:
        query = ''

    response = await review_service.get_reviews_by_query(
        query=query,
    )

    if response is None:
        logger.info('BAB_REQUEST_ERROR')
        raise HTTPStatus.BAD_REQUEST

    return response


@router.post(
    '/reviews',
    description='Метод создает новую рецензию',
)
async def set_review(
        document: ReviewModel = Body(),
        review_service: ReviewService = Depends(get_reviews_service),
) -> None:

    await review_service.set_data_by_document(
        document=document
    )


@router.put(
    '/reviews',
    description='Метод устанавливает лайк рецензии'
)
async def update_review(
        document: ReviewModel = Body(),
        review_service: ReviewService = Depends(get_reviews_service),
) -> None:

    await review_service.update_data_document(
        document=document,
    )
