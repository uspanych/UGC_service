from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(..., env='PROJECT_NAME')
    REDIS_HOST: str = Field(..., env='REDIS_HOST')
    REDIS_PORT: int = Field(..., env='REDIS_PORT')
    KAFKA_BOOTSTRAP_SERVERS: list = Field(..., env='KAFKA_BOOTSTRAP_SERVERS')
    TOPIC: str = Field(..., env='TOPIC')

    class Config:
        env_file = '.env'


settings = Settings()
