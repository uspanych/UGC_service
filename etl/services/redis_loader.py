from kafka import KafkaConsumer
from redis import Redis


class RedisLoader:
    """Класс закгрузки в редис.

    Класс предназначен для загрузки данных из Kafka в Redis
    """

    def __init__(
            self,
            consumer: KafkaConsumer,
            redis: Redis,
    ) -> None:
        self.consumer = consumer
        self.redis = redis

    def get_kafka_data(self, batch_size: int = 100):
        for message in self.consumer:
            print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key,
                                                 message.value))
