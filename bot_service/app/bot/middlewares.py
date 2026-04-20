import logging
from aiogram import BaseMiddleware
from aiogram.types import Message

logger = logging.getLogger(__name__)

# middleware  для логирования сообщений
class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event:Message, data):
        
            # логируем пользователя и текст
            user = event.from_user
            message_text = event.text or "[non-text]"
            short_text = message_text[:50] + "..." if len(message_text) > 50 else message_text
            logger.info(f"User {user.id}: {short_text}")
            return await handler(event, data)
