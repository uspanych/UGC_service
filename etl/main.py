from threading import Thread

from clickhouse_driver import Client
from kafka import KafkaConsumer
from redis import Redis

from core.config import settings
from services.clickhouse_loader import ClickHouseLoader
from services.redis_loader import RedisLoader


def etl_redis() -> None:
    """Функция инициализирует запуск переноса данных из Kafka в Redis."""
    loader = RedisLoader(
        consumer=KafkaConsumer(
            settings.TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
            group_id=settings.GROUP_ID_REDIS,
        ),
        redis=Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            charset='utf-8',
            decode_responses=True,
        )
    )

    while True:
        loader.get_kafka_data(
            batch_size=settings.BATCH_SIZE_REDIS,
        )


def etl_clickhouse() -> None:
    """Функция инициализирует запуск переноса данных из Kafka в ClickHouse"""
    clickhouse_loader = ClickHouseLoader(
        consumer=KafkaConsumer(
            settings.TOPIC,
            enable_auto_commit=False,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
            group_id=settings.GROUP_ID_CLICKHOUSE,
            consumer_timeout_ms=settings.TIMEOUT_CLICKHOUSE * 1000
        ),
        clickhouse=Client(settings.CLICKHOUSE_SERVER)
    )

    while True:
        clickhouse_loader.get_kafka_data(
            batch_size=settings.BATCH_SIZE_CLICKHOUSE
        )


if __name__ == '__main__':
    t1 = Thread(target=etl_redis)
    t1.start()
    t2 = Thread(target=etl_clickhouse)
    t2.start()
