from fastapi import FastAPI

from app.core.config import settings

# api для бота
app = FastAPI(
    title=settings.app_name,
    description="Telegram Bot для LLM-консультаций",
    version="1.0.0",
)

# проверка здоровья
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "env": settings.env,
    }
