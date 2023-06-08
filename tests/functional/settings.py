from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: list = Field(..., env='KAFKA_BOOTSTRAP_SERVERS')
    TOPIC: str = Field(..., env='TOPIC')
    GROUP_ID: str = Field(..., env='GROUP_ID')


test_settings = TestSettings()
