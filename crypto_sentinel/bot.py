import asyncio
import aiohttp
from aiogram import Bot,Dispatcher
import logging
from config_reader import config
from app.database.database import async_session, dispose_db, init_db, redis_client
from app.middlewares.database import DbSessionMiddleware

from app.handlers.user import user_router
from app.handlers.prices import price_router
from app.handlers.alerts import alerts_router
from app.handlers.settings import setting_router
from aiogram.utils.i18n import I18n
from app.middlewares.i18n import I18nMiddleware
from app.middlewares.database import DbSessionMiddleware
from app.database.database import async_session

i18n = I18n(path="locales", default_locale="en", domain="messages")

bot=Bot(token=config.bot_token.get_secret_value())
dp=Dispatcher()
dp.include_router(user_router)
dp.include_router(price_router)
dp.include_router(alerts_router)
dp.include_router(setting_router)

async def main():
    logging.basicConfig(level=logging.INFO)
    dp.update.outer_middleware(DbSessionMiddleware(session_pool=async_session))
    dp.update.outer_middleware(I18nMiddleware(i18n=i18n))
    await init_db()
    async with aiohttp.ClientSession() as http_session:
        dp.message.middleware(DbSessionMiddleware(async_session, redis_client, http_session))
        logging.info("Sentinel Crypto Bot started!")
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)
        finally:
            await dispose_db()

if __name__=="__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot turn off")


