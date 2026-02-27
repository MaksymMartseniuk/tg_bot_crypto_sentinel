import asyncio
from aiogram import Bot,Dispatcher
import logging
from config_reader import config
from app.database.database import init_db
from app.handlers.user import user_router
from app.handlers.prices import price_router
from app.handlers.alerts import alerts_router

bot=Bot(token=config.bot_token.get_secret_value())
dp=Dispatcher()
dp.include_router(user_router)
dp.include_router(price_router)
dp.include_router(alerts_router)

async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    await dp.start_polling(bot)

if __name__=="__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot turn off")


