from redis.asyncio import Redis

from app.core.config import settings


class RedisClient:
    def __init__(self):
        redis_params = {
            "host": settings.REDIS_HOST,
            "port": settings.REDIS_PORT,
            "decode_responses": True,
        }
        if settings.REDIS_PASSWORD:
            redis_params["password"] = settings.REDIS_PASSWORD
        self.redis = Redis(**redis_params)

    async def set_with_ttl(self, key: str, value: str, ttl_seconds: int):
        await self.redis.setex(key, ttl_seconds, value)

    async def get(self, key: str) -> str:
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def set_cooldown(self, key: str, ttl_seconds: int):
        await self.redis.setex(key, ttl_seconds, "1")

    async def check_cooldown(self, key: str) -> bool:
        return bool(await self.redis.exists(key))

    def pipeline(self, *args, **kwargs):
        return self.redis.pipeline(*args, **kwargs)

    async def brpop(self, key, timeout=1):
        return await self.redis.brpop(key, timeout=timeout)

    async def close(self):
        await self.redis.aclose()


redis_client = RedisClient()
