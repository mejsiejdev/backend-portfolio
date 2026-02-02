import redis.asyncio as aioredis

from core.config import get_settings

_pool: aioredis.ConnectionPool | None = None


async def initialize_redis_pool():
    global _pool
    settings = get_settings()
    _pool = aioredis.ConnectionPool.from_url(
        settings.redis_url, max_connections=50, decode_responses=True
    )


async def close_redis_pool():
    global _pool
    if _pool:
        await _pool.disconnect()
        _pool = None


def get_redis() -> aioredis.Redis:
    if _pool is None:
        raise RuntimeError("Redis pool not initialized.")
    return aioredis.Redis(connection_pool=_pool)
