import asyncio
from create_bot import bot, dp, logger, db
from handlers.callbacks import start_callback_router
from handlers.commands import start_cmd_router
from handlers.messages import start_msg_router
from aiogram.types import ErrorEvent

async def main():
    await db.connect()
    await db.create_tables()
    logger.info("Connected to database.")

    dp.include_router(start_callback_router)
    dp.include_router(start_cmd_router)
    dp.include_router(start_msg_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


@dp.errors()
async def error_handler(event: ErrorEvent):
    logger.error("Unhandled exception was thrown by %s", event.update, exc_info=event.exception)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped.')
