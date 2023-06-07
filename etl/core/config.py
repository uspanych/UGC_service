from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    REDIS_HOST: str = Field(..., env='REDIS_HOST')
    REDIS_PORT: int = Field(..., env='REDIS_PORT')
    KAFKA_BOOTSTRAP_SERVER: list = Field(..., env='KAFKA_BOOTSTRAP_SERVERS')
    TOPIC: str = Field(..., env='TOPIC')
    GROUP_ID_REDIS: str = Field(..., env='GROUP_ID_REDIS')
    TTL_REDIS: str = Field(..., env='TTL')
    BATCH_SIZE_REDIS: int = Field(..., env='BATCH_SIZE_REDIS')
    GROUP_ID_CLICKHOUSE: str = Field(..., env='GROUP_ID_CLICKHOUSE')
    BATCH_SIZE_CLICKHOUSE: int = Field(..., env='BATCH_SIZE_CLICKHOUSE')
    TIMEOUT_CLICKHOUSE: int = Field(..., env='TIMEOUT_CLICKHOUSE')
    CLICKHOUSE_SERVER: str = Field(..., env='CLICKHOUSE_SERVER')

    class Config:
        env_file = '.env'


settings = Settings()
