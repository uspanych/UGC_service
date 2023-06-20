from typing import Optional
from redis.asyncio import Redis


redis: Redis | None = None


async def get_redis() -> Optional[Redis]:
    return redis
