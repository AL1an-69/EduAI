from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv
import asyncio

from handlers import router

load_dotenv()

async def main():
    bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
