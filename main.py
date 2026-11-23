import asyncio
import logging
from bot.handlers.start import router as start_router
from bot.handlers.habits import router as habits_router
from bot.handlers.callbacks import router as callbacks_router


from aiogram import Bot, Dispatcher

from config.settings import settings

async def main():

    # configure logging
    logging.basicConfig(level=logging.INFO)

    # create bot instance
    bot = Bot(token=settings.BOT_TOKEN)

    # create dispatcher
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(callbacks_router)
    dp.include_router(habits_router)

    print("Habit tracker is starting...")

    try:
        await dp.start_polling(bot)

    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())