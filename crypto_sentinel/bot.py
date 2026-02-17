import asyncio
from aiogram import Bot,Dispatcher
import logging
from config_reader import config
async def main():
    logging.basicConfig(level=logging.INFO)
    bot=Bot(token=config.bot_token.get_secret_value())
    dp=Dispatcher()
    await dp.start_polling(bot)

if __name__=="__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot turn off")


