from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, Response, HTTPException
from async_fastapi_jwt_auth import AuthJWT

from models.views import ViewModel, ViewResponseModel
from services.utils.token_verify import role_required
from services.views import ViewsService, get_views_service
from fastapi.logger import logger

router = APIRouter()


@router.post(
    '/views',
    description="Метод сохраняет временную метку просмотра фильма",
)
async def views_set_time(
        views_service: ViewsService = Depends(get_views_service),
        views: ViewModel = Body(...),
        autorize: AuthJWT = Depends(),
) -> int:

    # await role_required(autorize, ["User", "SuperUser", "Admin"])

    try:
        await views_service.set_data_key(
            key=views.key,
            value=views.value,
        )
        return Response(status_code=HTTPStatus.OK)
    except Exception as error:
        logger.info(f'Set for base error {error}')
        raise HTTPException(HTTPStatus.BAD_REQUEST)


@router.get(
    '/views',
    response_model=ViewResponseModel,
    description='Метод возвращает кадр фильма',
)
async def views_get_time(
        key: str,
        views_service: ViewsService = Depends(get_views_service),
        autorize: AuthJWT = Depends(),
) -> ViewResponseModel | HTTPStatus:

    # await role_required(autorize, ["SuperUser", "Admin", "User"])

    try:
        response = await views_service.get_data_key(key)
        return response
    except Exception as error:
        logger.info(f'Query for base error {error}')
        raise HTTPException(HTTPStatus.BAD_REQUEST)

