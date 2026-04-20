import logging
import redis.asyncio as redis_async
import redis
from app.core.config import settings

logger = logging.getLogger(__name__)

# клиенты редиса
redis_async_client = None
redis_sync_client = None

# для бота
def get_redis():
    global redis_async_client

    if redis_async_client is None:
        redis_async_client = redis_async.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=False
        )

    return redis_async_client


# для воркера
def get_redis_sync():
        global redis_sync_client

        if redis_sync_client is None:
            redis_sync_client = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=False
            )

        return redis_sync_client

# закрытие соединения
async def close_redis():
    global redis_async_client

    if redis_async_client is not None:
        await redis_async_client.aclose()
        redis_async_client = None
