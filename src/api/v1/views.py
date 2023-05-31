from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.views import ViewResponseModel

router = APIRouter()


@router.post(
    '/views',
    description="Метод сохраняет временную метку просмотра фильма",
)
async def views_set_time(
        key: str,
        value: str,
):
    pass