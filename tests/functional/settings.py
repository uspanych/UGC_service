from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: list = Field(..., env='KAFKA_BOOTSTRAP_SERVERS')
    TOPIC: str = Field(..., env='TOPIC')
    SERVICE_URL: str = "http://web:8000"


test_settings = TestSettings()
