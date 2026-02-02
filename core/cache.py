import functools
import hashlib
import json
from typing import Callable

from core.config import get_settings
from core.redis import get_redis


def cached(ttl_seconds: int | None = None, prefix: str = "cache"):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            settings = get_settings()
            ttl = ttl_seconds or settings.cache_ttl

            key_data = f"{func.__module__}.{func.__name__}:{args}:{kwargs}"
            key_hash = hashlib.sha256(key_data.encode()).hexdigest()
            cache_key = f"{prefix}:{func.__name__}:{key_hash}"

            redis = get_redis()

            if cached_data := await redis.get(cache_key):
                return json.loads(cached_data)

            result = await func(*args, **kwargs)
            await redis.setex(cache_key, ttl, json.dumps(result))
            return result

        return wrapper

    return decorator


async def invalidate_cache(pattern: str = "cache:*") -> int:
    redis = get_redis()
    keys = [key async for key in redis.scan_iter(match=pattern)]
    if keys:
        return await redis.delete(*keys)
    return 0
