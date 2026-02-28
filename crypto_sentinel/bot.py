import asyncio
from aiogram import Bot,Dispatcher
import logging
from config_reader import config
from app.database.database import async_session, dispose_db, init_db
from app.middlewares.database import DbSessionMiddleware

from app.handlers.user import user_router
from app.handlers.prices import price_router
from app.handlers.alerts import alerts_router
from app.handlers.settings import setting_router

bot=Bot(token=config.bot_token.get_secret_value())
dp=Dispatcher()
dp.include_router(user_router)
dp.include_router(price_router)
#dp.include_router(alerts_router)
#dp.include_router(setting_router)

async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    dp.message.middleware(DbSessionMiddleware(async_session))
    try:
        await dp.start_polling(bot)
    finally:
        await dispose_db()

if __name__=="__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot turn off")


