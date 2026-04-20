from celery import Celery
from app.core.config import settings

# настройка celery
celery_app = Celery(
    "bot_service",
    broker=settings.rabbitmq_url,
    backend=settings.redis_url,
    include=["app.tasks.llm_tasks"]
)
