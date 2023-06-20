from models.base import BaseOrjsonModel
from pydantic import Field, BaseModel
from datetime import datetime
from uuid import uuid4, UUID
from .base import PyObjectId
from bson import ObjectId


class LikesModel(BaseOrjsonModel):
    user_id: str
    film_id: str
    point: int


class FilmResponseModel(BaseOrjsonModel):
    film_id: str
    positive_vote: int
    negative_vote: int


class FilmAvgModel(BaseOrjsonModel):
    film_id: str
    avg_vote: float


class ReviewModel(BaseModel):
    review_id: str = Field(default_factory=uuid4)
    user_id: str
    film_id: str
    review: str
    date: datetime = Field(default_factory=datetime.now)
    like: str | None = None


class BookmarksModel(BaseModel):
    user_id: str
    film_id: str
