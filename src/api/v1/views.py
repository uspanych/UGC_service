from http import HTTPStatus

from fastapi import APIRouter, Depends, Body
from services.views import get_views_service, ViewsService
from models.views import ViewModel

router = APIRouter()


@router.post(
    '/views',
    description="Метод сохраняет временную метку просмотра фильма",
)
async def views_set_time(
        views_service: ViewsService = Depends(get_views_service),
        views: ViewModel = Body(...)
) -> None:

    views = await views_service.set_data_key(
        key=views.key,
        value=views.value,
    )
