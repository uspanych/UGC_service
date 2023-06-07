from logging import config as logging_config

from fastapi_jwt_auth import AuthJWT

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

from pydantic import BaseSettings, Field, BaseModel



class Settings(BaseSettings):
    PROJECT_NAME: str = Field(..., env='PROJECT_NAME')
    REDIS_HOST: str = Field(..., env='REDIS_HOST')
    REDIS_PORT: int = Field(..., env='REDIS_PORT')
    KAFKA_BOOTSTRAP_SERVERS: list = Field(..., env='KAFKA_BOOTSTRAP_SERVERS')
    TOPIC: str = Field(..., env='TOPIC')
    SECRET_KEY: str = Field(..., env='SECRET_KEY')

    class Config:
        env_file = '.env'

    def get_public_key(self):
        with open(settings.SECRET_KEY) as pbk:
            return pbk.read()


settings = Settings()


class AuthJWTSetting(BaseModel):
    authjwt_public_key: str = settings.get_public_key()
    authjwt_algorithm: str = "RS256"
    authjwt_token_location: set = {"cookies", "headers"}


@AuthJWT.load_config
def get_config():
    return AuthJWTSetting()
