import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.handlers import router

async def main():
    load_dotenv()

    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("Bot token not found in .env file")

    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_router(router)

    logging.info("Bot is starting...")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())