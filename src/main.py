from uuid import uuid4

import logstash
import sentry_sdk
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, Request
from fastapi.logger import logger
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

from api.v1 import bookmarks, likes, review, views
from core.config import settings
from db import kafka, mongo, redis

logstash_handler = logstash.LogstashHandler('logstash', 5044, version=1)
logger.addHandler(logstash_handler)


sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    request_id = response.headers.get("X-Request-Id")
    if request_id is None:
        response.headers["X-Request-Id"] = str(uuid4())
    return response


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


@app.get("/test")
async def test():
    logger.info('Test function!')
    return {
        "message": "Hello world!"
    }


app.include_router(views.router, prefix='/api/v1/views', tags=['views'])
app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(review.router, prefix='/api/v1/reviews', tags=['reviews'])
app.include_router(
    bookmarks.router, prefix='/api/v1/bookmarks', tags=['bookmarks'])
