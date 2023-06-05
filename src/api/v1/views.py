from http import HTTPStatus

from fastapi import APIRouter, Depends, Body
from services.views import get_views_service, ViewsService
from models.views import ViewModel, ViewResponseModel

router = APIRouter()


@router.post(
    '/views',
    description="Метод сохраняет временную метку просмотра фильма",
)
async def views_set_time(
        views_service: ViewsService = Depends(get_views_service),
        views: ViewModel = Body(...)
) -> int:

    try:
        await views_service.set_data_key(
            key=views.key,
            value=views.value,
        )

        return HTTPStatus.OK

    except:

        return HTTPStatus.BAD_REQUEST


@router.get(
    '/views',
    response_model=ViewResponseModel,
    description='Метод возвращает кадр фильма',
)
async def views_get_time(
        key: str,
        views_service: ViewsService = Depends(get_views_service),
) -> ViewResponseModel:

    response = await views_service.get_data_key(key)

    return response
