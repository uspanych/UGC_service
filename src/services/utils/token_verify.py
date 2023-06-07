from http import HTTPStatus

from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT


def role_required(auth: AuthJWT, roles: list):
    try:
        auth.jwt_required()
    except Exception:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Токен не валиден")
    role = auth.get_raw_jwt().get("role")

    if role not in roles:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Доступ запрещен")