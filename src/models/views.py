from enum import Enum
from datetime import datetime
from models.base import BaseOrjsonModel


class ViewModel(BaseOrjsonModel):
    id: bytes
    value: bytes
