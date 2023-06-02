from models.base import BaseOrjsonModel


class ViewModel(BaseOrjsonModel):
    key: bytes
    value: bytes
