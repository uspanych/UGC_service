import time

from kafka import KafkaConsumer
from services.redis_loader import RedisLoader
from core.config import settings
from redis import Redis


def etl():
    loader = RedisLoader(
        consumer=KafkaConsumer(
            settings.TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
            group_id=settings.GROUP_ID,
        ),
        redis=Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
        )
    )

    while True:
        time.sleep(15)
        loader.get_kafka_data()


if __name__ == '__main__':
    etl()
