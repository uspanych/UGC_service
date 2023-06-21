from contextlib import asynccontextmanager
from uuid import uuid4

import logstash
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.logger import logger
from fastapi.responses import ORJSONResponse

from api.v1 import bookmarks, likes, review, views
from core.config import settings
from services.utils.lifespan import startup, shutdown

logstash_handler = logstash.LogstashHandler(settings.LOGSTASH_HOST, settings.LOGSTASH_PORT, version=1)
logger.addHandler(logstash_handler)


sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(
    lifespan=lifespan,
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


app.include_router(views.router, prefix='/api/v1/views', tags=['views'])
app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(review.router, prefix='/api/v1/reviews', tags=['reviews'])
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['bookmarks'])
