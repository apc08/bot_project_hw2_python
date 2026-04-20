import logging

from app.infra.celery_app import celery_app
from app.services.openrouter_client import OpenRouterSyncClient
from app.infra.redis_operations import save_llm_result_sync
from app.core.exceptions import OpenRouterError

logger = logging.getLogger(__name__)


# задача для запроса к llm
@celery_app.task(
    name="llm_request",
    bind=True,
    autoretry_for=(OpenRouterError,),
    max_retries=3,
    default_retry_delay=5,
)
def llm_request(self, tg_user_id, prompt):
    task_id = self.request.id

    try:
        # запрос к openrouter
        client = OpenRouterSyncClient()
        messages = [{"role": "user", "content": prompt}]
        response = client.chat(messages)

        save_llm_result_sync(tg_user_id, task_id, response)
        return response
        

    except OpenRouterError as e:
        error_msg = f"Ошибка при обращении к LLM:  {str(e)}"

        if self.request.retries >= self.max_retries:
            save_llm_result_sync(tg_user_id, task_id, error_msg)

        raise


    except Exception as e:
        error_msg = f"неожиданная ошибка при обработке запроса: {str(e)}"
        save_llm_result_sync(tg_user_id, task_id, error_msg)
        raise
