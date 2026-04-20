import asyncio
import logging
from functools import partial
from app.bot.dispatcher import create_bot, create_dispatcher, on_startup, on_shutdown

# логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# запуск бота
async def main():
    logger.info("Starting Bot Service...")

    bot = create_bot()
    dp = create_dispatcher()

    dp.startup.register(partial(on_startup, bot))
    dp.shutdown.register(partial(on_shutdown, bot))

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        logger.info("Bot stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C)")
