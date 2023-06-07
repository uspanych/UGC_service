from models.base import BaseOrjsonModel
import uuid as uuid_pkg


class ViewModel(BaseOrjsonModel):
    key: str
    value: str


class ClickHouseModel(BaseOrjsonModel):
    user_id: uuid_pkg.UUID
    movie_id: uuid_pkg.UUID
    viewed_frame: int
