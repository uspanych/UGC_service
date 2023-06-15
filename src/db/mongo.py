from motor.motor_asyncio import AsyncIOMotorClient

client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    return client
