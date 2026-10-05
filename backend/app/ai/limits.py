from pydantic_ai.usage import UsageLimits

from app.core.redis import get_redis

# Hard per-run cap so a looping tool call cannot burn tokens.
CHAT_LIMITS = UsageLimits(request_limit=5)


async def allow(key: str, limit: int = 30, window_s: int = 60) -> bool:
    """Fixed-window rate limit backed by Redis INCR."""
    redis = get_redis()
    try:
        n = await redis.incr(f"rl:{key}")
        if n == 1:
            await redis.expire(f"rl:{key}", window_s)
        return int(n) <= limit
    finally:
        await redis.aclose()
