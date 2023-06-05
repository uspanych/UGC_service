from kafka import KafkaConsumer
from services.redis_loader import RedisLoader
from core.config import settings
from redis import Redis


def etl() -> None:
    """Функция инициализирует запуск переноса данных из Kafka в Redis."""
    loader = RedisLoader(
        consumer=KafkaConsumer(
            settings.TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
            group_id=settings.GROUP_ID,
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
            batch_size=settings.BATCH_SIZE,
        )


if __name__ == '__main__':
    etl()
