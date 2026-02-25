import aiohttp
import logging
from app.database.database import redis_client

logger=logging.getLogger(__name__)

async def get_crypto_price(symbol:str="BTC"):
    pair=f"{symbol.upper()}USDT"
    redis_key = f"price:{pair}"
    cached_price=await redis_client.get(redis_key)
    if cached_price:
        return float(cached_price)
    url = f"https://api4.binance.com/api/v3/ticker/price?symbol={pair}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url,timeout=5) as response:
                if response.status==200:
                    data= await response.json()
                    price=float(data['price'])
                    await redis_client.set(redis_key, price, ex=30)
                    return price
                if response.status==400:
                    logger.error(f"Unfaithful couple: {pair}")
                    return None
                else:
                    logger.error(f"Error Binance API: {response.status}")
                    return None
    except Exception as e:
        logger.error(f"Error when requesting Binance: {e}")
        return None