import pytest
from app.services.binance_api import get_crypto_price

@pytest.mark.parametrize("symbol",[
    "BTC",
    "ETH",
    "SOL"
])

async def test_binance_api(symbol):
    
    assert await get_crypto_price(symbol) is not None