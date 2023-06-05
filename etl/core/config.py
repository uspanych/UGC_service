from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    REDIS_HOST: str = Field(..., env='REDIS_HOST')
    REDIS_PORT: int = Field(..., env='REDIS_PORT')
    KAFKA_BOOTSTRAP_SERVER: list = Field(..., env='KAFKA_BOOTSTRAP_SERVERS')
    TOPIC: str = Field(..., env='TOPIC')
    GROUP_ID: str = Field(..., env='GROUP_ID')
    TTL_REDIS: str = Field(..., env='TTL')
    BATCH_SIZE: int = Field(..., env='BATCH_SIZE')

    class Config:
        env_file = '.env'


settings = Settings()
