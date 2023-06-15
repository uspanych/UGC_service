from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import views, likes, review, bookmarks
from core.config import settings
from db import kafka, redis, mongo

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup() -> None:
    redis.redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
    )

    kafka.producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
    )

    mongo.client = AsyncIOMotorClient(
        f'mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}'
    )

    await kafka.producer.start()


@app.on_event("shutdown")
async def shutdown() -> None:
    await redis.redis.close()
    await kafka.producer.stop()


app.include_router(views.router, prefix='/api/v1/views', tags=['views'])
app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(review.router, prefix='/api/v1/reviews', tags=['reviews'])
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['bookmarks'])
