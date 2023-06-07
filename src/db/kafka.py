from aiokafka import AIOKafkaProducer

producer: AIOKafkaProducer | None


def get_producer() -> AIOKafkaProducer:
    return producer
