import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.config import BOT_TOKEN
from app.database.database import init_db

# Handlers
from app.handlers import start, marketplace, selling, buying, profile, disputes, admin

async def main():
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is not set in environment variables!")
        sys.exit(1)

    logging.basicConfig(level=logging.INFO)
    
    # Initialize Database
    await init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Include routers
    dp.include_router(start.router)
    dp.include_router(marketplace.router)
    dp.include_router(selling.router)
    dp.include_router(buying.router)
    dp.include_router(profile.router)
    dp.include_router(disputes.router)
    dp.include_router(admin.router)

    logging.info("Bot started successfully!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
