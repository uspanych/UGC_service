from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

producer: AIOKafkaProducer | None


def get_producer() -> AIOKafkaProducer:
    return producer
