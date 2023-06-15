from fastapi import APIRouter, Body, Depends
from http import HTTPStatus
from services.likes import LikesService, get_likes_service
from models.mongo import LikesModel, FilmResponseModel, FilmAvgModel

router = APIRouter()


@router.get(
    '/likes/film',
    description='Метод возвращает информацию по фильму',
    response_model=FilmResponseModel,
)
async def get_document_like(
    film_id: str,
    likes_service: LikesService = Depends(get_likes_service),
) -> FilmResponseModel:

    response = await likes_service.get_data_by_film(
        query={'film_id': film_id},
    )
    if response is None:
        raise HTTPStatus.BAD_REQUEST

    return response


@router.get(
    '/likes/avg',
    description='Метод возвращает среднюю оценку по фильму',
    response_model=FilmAvgModel,
)
async def get_avg_like(
        film_id: str,
        likes_service: LikesService = Depends(get_likes_service),
) -> FilmAvgModel:

    response = await likes_service.get_avg_likes(
        query={'film_id': film_id},
    )

    if response is None:
        raise HTTPStatus.BAD_REQUEST

    return response


@router.put(
    '/like/update',
    description='Метод обновляет инофрмацию о лайке'
)
async def update_document_like(
        like_service: LikesService = Depends(get_likes_service),
        document: LikesModel = Body(),
) -> None:

    await like_service.update_data_by_document(
        document=document
    )


@router.delete(
    '/like/delete',
    description='Метод позволяет удалить информацию о лайке',
)
async def delete_document_like(
        film_id: str,
        like_service: LikesService = Depends(get_likes_service),
) -> None:

    await like_service.delete_data_by_document(
        query={'film_id': film_id}
    )


@router.post(
    '/like',
    description='Метод сохраняет документ в базы'
)
async def set_document_like(
    likes_service: LikesService = Depends(get_likes_service),
    document: LikesModel = Body(),
) -> None:

    await likes_service.set_data_by_document(
        document=document,
    )
