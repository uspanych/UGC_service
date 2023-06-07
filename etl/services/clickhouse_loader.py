from kafka import KafkaConsumer
from clickhouse_driver import Client

from core.config import settings
from models.views import ClickHouseModel


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

    def get_kafka_data(self, batch_size: int = 1) -> None:
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

    def _set_data_in_clickhouse(self, cash):
        query = self.SQL_CREATE_RECORD.format(
            data=", ".join([f"('{i.user_id}', '{i.movie_id}', {i.viewed_frame})" for i in cash])
        )
        print(query)
        self.clickhouse.execute(query)
