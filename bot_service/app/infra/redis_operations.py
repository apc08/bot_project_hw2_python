import logging
from app.core.config import settings
from app.infra.redis import get_redis, get_redis_sync

logger = logging.getLogger(__name__)

#£ сохранить токен в redis
async def save_user_token(user_id, token):
    redis_client = get_redis()
    key = f"user_token:{user_id}"
    await redis_client.set(key, token, ex=settings.token_ttl)


async def get_user_token(user_id):
    redis_client = get_redis()
    key = f"user_token:{user_id}"
    token = await redis_client.get(key)
    return token

async def delete_user_token(user_id):
    redis_client = get_redis()
    key = f"user_token:{user_id}"
    await redis_client.delete(key)

# получить результат от llm
async def get_llm_result(user_id, task_id):
    redis_client = get_redis()
    key = f"llm_result:{user_id}:{task_id}"
    result = await redis_client.get(key)
    return result

async def delete_llm_result(user_id, task_id):
    redis_client = get_redis()
    key = f"llm_result:{user_id}:{task_id}"
    await redis_client.delete(key)


# для celery worker
def save_llm_result_sync(user_id, task_id, result):
    
    redis_client = get_redis_sync()
    key = f"llm_result:{user_id}:{task_id}"
    redis_client.set(key, result, ex=settings.result_ttl)
