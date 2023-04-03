"""Imports"""
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import default_commands, new_conv


load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
print(BOT_TOKEN)


logging.basicConfig(level=logging.INFO)


async def main():
    """Initializing the boy"""
    dp = Dispatcher()

    dp.include_router(default_commands.router)
    dp.include_router(new_conv.router)

    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
