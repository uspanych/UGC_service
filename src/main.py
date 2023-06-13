import sentry_sdk

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import views
from core.config import settings
from db import kafka, redis


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

    await kafka.producer.start()


@app.on_event("shutdown")
async def shutdown() -> None:
    await redis.redis.close()
    await kafka.producer.stop()


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


app.include_router(views.router, prefix='/api/v1/views', tags=['views'])
