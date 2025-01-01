from redis.asyncio import Redis

from config import REDIS_HOST, REDIS_PORT, MESSAGE_LIMIT, TIME_WINDOW_SECONDS


redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def is_request_allowed(user_id: int) -> tuple[bool, int]:
    
    allowed, ttl = await check_limit(user_id)

    if not allowed:
            return False, ttl

    redis_key = f"user_requests:{user_id}"
    pipeline = redis.pipeline()
    pipeline.incr(redis_key)
    pipeline.expire(redis_key, TIME_WINDOW_SECONDS)
    await pipeline.execute()

    return True, 0


async def check_limit(user_id: int) -> tuple[bool, int]:
    redis_key = f"user_requests:{user_id}"
    current_count = await redis.get(redis_key)
    
    if current_count is not None and int(current_count) >= MESSAGE_LIMIT:
        ttl = await redis.ttl(redis_key)
        return False, ttl

    return True, 0