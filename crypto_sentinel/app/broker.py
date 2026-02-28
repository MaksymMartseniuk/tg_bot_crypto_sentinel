import asyncio
import aiohttp
import taskiq_aiogram 
from aiogram import Bot
from taskiq import TaskiqDepends,TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import ListQueueBroker
from config_reader import config
from app.database.requests import get_active_alerts
from app.services.binance_api import get_crypto_price
from app.database.database import get_session


redis_url = f"redis://{config.redis_host.get_secret_value()}:{config.redis_port.get_secret_value()}/0"
broker=ListQueueBroker(redis_url)
taskiq_aiogram.init(
    broker,
    "bot:dp",
    "bot:bot"
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


@broker.task(task_name="check_crypto_alerts", schedule=[{'cron': '*/1 * * * *'}])
async def check_crypto_alerts(bot: Bot = TaskiqDepends(),session = TaskiqDepends(get_session)) -> None:
    alerts = await get_active_alerts(session)
    if not alerts:
        return
    async with aiohttp.ClientSession() as http_session:
        for alert in alerts:
            current_price = await get_crypto_price(alert.symbol,http_session=http_session)
            if current_price is None:
                continue

        triggered = False
        if alert.direction == "UP" and current_price >= alert.target_price:
                triggered = True
        elif alert.direction == "DOWN" and current_price <= alert.target_price:
                triggered = True

        if triggered:
            try:
                emoji = "📈" if alert.direction == "UP" else "📉"
                text = (
                    f"{emoji} <b>Alert Triggered!</b>\n\n"
                    f"Asset: <b>{alert.symbol}</b>\n"
                    f"Target: <code>${alert.target_price:,.2f}</code>\n"
                    f"Current: <code>${current_price:,.2f}</code>"
                    )
                await bot.send_message(alert.user.tg_id, text, parse_mode="HTML") 
                alert.is_active = False
                session.add(alert)
            except Exception as e:
                    print(f"Failed to notify {alert.user.tg_id}: {e}")
    await session.commit()
    
