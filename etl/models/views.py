from models.base import BaseOrjsonModel


class ViewModel(BaseOrjsonModel):
    key: str
    value: str
