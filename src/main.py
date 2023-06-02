from db import redis
from db import kafka
from fastapi import FastAPI
from core.config import settings
from redis.asyncio import Redis
from aiokafka import AIOKafkaProducer
from fastapi.responses import ORJSONResponse
from api.v1 import views

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT
    )

    kafka.producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
    )

    await kafka.producer.start()


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await kafka.producer.stop()


app.include_router(views.router, prefix='/api/v1/views', tags=['views'])
