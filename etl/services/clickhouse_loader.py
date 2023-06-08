from clickhouse_driver import Client
from kafka import KafkaConsumer

from models.views import ClickHouseModel
from services.backoff import backoff


class ClickHouseLoader:
    """Класс загрузки в ClickHouse"""

    SQL_CREATE_RECORD = """
    INSERT INTO default.test (user_id, movie_id, viewed_frame) VALUES {data};
    """

    def __init__(
            self,
            consumer: KafkaConsumer,
            clickhouse: Client
    ) -> None:
        self.consumer = consumer
        self.clickhouse = clickhouse

    @backoff()
    def get_kafka_data(self, batch_size: int = 1000) -> None:
        cash = []
        for message in self.consumer:
            user_id, movie_id = message.key.decode().split("+")
            cash.append(ClickHouseModel(
                user_id=user_id,
                movie_id=movie_id,
                viewed_frame=message.value.decode()
            ))
            if len(cash) >= batch_size:
                self._set_data_in_clickhouse(cash)
        if cash:
            self._set_data_in_clickhouse(cash)

    @backoff()
    def _set_data_in_clickhouse(self, cash):
        query = self.SQL_CREATE_RECORD.format(
            data=", ".join([f"('{i.user_id}', '{i.movie_id}', {i.viewed_frame})" for i in cash])
        )
        self.clickhouse.execute(query)
