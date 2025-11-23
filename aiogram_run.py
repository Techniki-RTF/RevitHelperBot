import asyncio
from create_bot import bot, dp, logger
from handlers.callbacks import start_callback_router
from handlers.commands import start_cmd_router
from aiogram.types import ErrorEvent

async def main():
    dp.include_router(start_callback_router)
    dp.include_router(start_cmd_router)
    await dp.start_polling(bot)


@dp.errors()
async def error_handler(error_event: ErrorEvent):
    logger.error(f"Необработанное исключение: {error_event.exception}")
    return None


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Бот остановлен')
