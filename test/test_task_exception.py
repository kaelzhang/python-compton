import asyncio
import pytest

from compton import (
    Orchestrator
)

from .types import (
    SimpleProvider,
    SimpleProvider3,
    SimpleProvider4,
    SimpleReducer,
    SimpleConsumer3,
    symbol
)


@pytest.mark.asyncio
async def test_process_error(caplog):
    Orchestrator(
        [SimpleReducer()]
    ).connect(
        SimpleProvider().go()
    ).subscribe(
        SimpleConsumer3()
    ).add(symbol)

    await asyncio.sleep(1)

    assert caplog.text.count('you got me') == 3


@pytest.mark.asyncio
async def test_provider_init_error(caplog):
    Orchestrator(
        [SimpleReducer()]
    ).connect(
        SimpleProvider3().go()
    ).add(symbol)

    await asyncio.sleep(1)

    assert caplog.text.count('you got me') == 4
    assert caplog.text.count('give up') == 1


@pytest.mark.asyncio
async def test_provider_when_update_error(caplog):
    Orchestrator(
        [SimpleReducer()]
    ).connect(
        SimpleProvider4().go()
    ).add(symbol)

    await asyncio.sleep(1)

    assert caplog.text.count('background task error: you got me') == 1
