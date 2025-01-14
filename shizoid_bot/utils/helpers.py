from redis.asyncio import Redis

from config import GROUP_CHAT_MESSAGE_LIMIT

async def check_limit(user_id: int, redis: Redis) -> tuple[bool, int]:
    redis_key = f"user_requests:{user_id}"
    current_count = await redis.get(redis_key)
    
    if current_count is not None and int(current_count) >= GROUP_CHAT_MESSAGE_LIMIT:
        ttl = await redis.ttl(redis_key)
        return False, ttl

    return True, 0