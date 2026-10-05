from redis.asyncio import Redis

from app.core.settings import get_settings


def get_redis() -> Redis:
    client: Redis = Redis.from_url(get_settings().redis_url)
    return client
