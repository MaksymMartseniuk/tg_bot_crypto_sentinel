import asyncio
import aiohttp
from aiogram import Bot,Dispatcher
import logging
from config_reader import config
from app.database.database import async_session, dispose_db, init_db, redis_client
from app.middlewares.database import DbSessionMiddleware

from app.i18n import i18n

from app.middlewares.i18n import I18nMiddleware
from app.middlewares.database import DbSessionMiddleware
from app.database.database import async_session

from app.handlers.user import user_router
from app.handlers.prices import price_router
from app.handlers.alerts import alerts_router
from app.handlers.settings import setting_router
from app.handlers.common import common_router

bot=Bot(token=config.bot_token.get_secret_value())
dp=Dispatcher()
dp.include_router(user_router)
dp.include_router(price_router)
dp.include_router(alerts_router)
dp.include_router(setting_router)
dp.include_router(common_router)

async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    async with aiohttp.ClientSession() as http_session:
        dp.update.outer_middleware(
            DbSessionMiddleware(session_pool=async_session,
                                redis=redis_client,
                                http_session=http_session
                                ))
        dp.update.outer_middleware(I18nMiddleware(i18n=i18n))
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


