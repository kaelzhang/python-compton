import asyncio
import pytest

from compton import (
    Orchestrator
)

from .types import (
    SimpleProvider,
    SimpleReducer,
    SimpleConsumer3,
    symbol
)


@pytest.mark.asyncio
async def test_process_error(caplog):
    consumer = SimpleConsumer3()
    provider = SimpleProvider().go()

    Orchestrator(
        [SimpleReducer()]
    ).connect(
        provider
    ).subscribe(
        consumer
    ).add(symbol)

    await asyncio.sleep(1)

    assert caplog.text.count('you got me') == 3
