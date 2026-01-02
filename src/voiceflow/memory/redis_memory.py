from redis.asyncio import Redis
import json
from voiceflow.config import get_settings

settings = get_settings()


class RedisMemory:
    def __init__(self) -> None:
        self.redis = Redis.from_url(
            settings.redis_url,
            decode_responses=True
        )
    
    async def save_exchange(self, session_id: str, user: str, ai: str) -> None:
        key = f"conversation:{session_id}:history"
        exchange = {"user": user, "ai": ai}
        await self.redis.lpush(key, json.dumps(exchange))
        await self.redis.ltrim(key, 0, 9)
        await self.redis.expire(key, 86400)
    
    async def get_history(self, session_id: str) -> list[dict]:
        key = f"conversation:{session_id}:history"
        history = await self.redis.lrange(key, 0, -1)
        return [json.loads(item) for item in history]
    
    async def get_context(self, session_id: str) -> dict:
        key = f"conversation:{session_id}:context"
        data = await self.redis.get(key)
        return json.loads(data) if data else {}
    
    async def save_context(self, session_id: str, context: dict) -> None:
        key = f"conversation:{session_id}:context"
        await self.redis.set(key, json.dumps(context), ex=86400)
    
    async def close(self) -> None:
        await self.redis.close()
