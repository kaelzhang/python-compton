import pytest

from compton.app.config import (
    FUTU_HOST,
    FUTU_PORT
)

from .mock_provider import MockProvider
from compton.quant.stock_manager import StockManager

code = 'HK.00700'

provider = MockProvider(code, FUTU_HOST, FUTU_PORT)
stock = StockManager(provider)


@pytest.mark.asyncio
async def test_main():
    provider.start()

    a, b, c = stock.subscribe([code])

    await
