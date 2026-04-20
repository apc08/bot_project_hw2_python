import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.core.config import settings
from app.bot.middlewares import LoggingMiddleware
from app.bot import handlers
from app.infra.redis import close_redis

logger = logging.getLogger(__name__)

# создание бота
def create_bot():

    return Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
             )
    )


# диспетчер с мидлварами
def create_dispatcher():

    dp = Dispatcher()
    dp.message.middleware(LoggingMiddleware())
    dp.include_router(handlers.router)

    return dp


# запуск бота
async def on_startup(bot:Bot):
    me = await bot.get_me()
    logger.info(f"Bot @{me.username} started (ID: {me.id})")



# закрытие соединений
async def on_shutdown(bot:Bot):
    await bot.session.close()
    await close_redis()
