from http import HTTPStatus

from fastapi import HTTPException
from async_fastapi_jwt_auth import AuthJWT


async def role_required(auth: AuthJWT, roles: list):
    try:
        await auth.jwt_required()
    except Exception:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Токен не валиден")
    role = (await auth.get_raw_jwt()).get("role")

    if role not in roles:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Доступ запрещен")
