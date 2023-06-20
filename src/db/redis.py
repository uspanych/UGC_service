from typing import Any, Optional
from redis.asyncio import Redis


redis: Redis | None = None


async def get_redis() -> Optional[Redis[Any]]:
    return redis
