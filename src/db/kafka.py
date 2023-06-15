from aiokafka import AIOKafkaProducer

producer: AIOKafkaProducer | None = None


def get_producer() -> AIOKafkaProducer:
    return producer
