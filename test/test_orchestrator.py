import asyncio
import pytest

from compton import (
    Orchestrator
)

from .types import (
    SimpleProvider,
    SimpleReducer,
    SimpleConsumer,
    symbol,
    vector
)


@pytest.mark.asyncio
async def test_main():
    consumer = SimpleConsumer()
    provider = SimpleProvider().go()

    Orchestrator(
        [SimpleReducer()]
    ).connect(
        provider
    ).subscribe(
        consumer
    ).add(symbol)

    await asyncio.sleep(1)

    assert consumer.consumed == [0, 1, 2]


@pytest.mark.asyncio
async def test_main_with_deferred_init():
    consumer = SimpleConsumer()
    provider = SimpleProvider()

    Orchestrator(
        [SimpleReducer()]
    ).connect(
        provider
    ).subscribe(
        consumer
    ).add(symbol)

    await asyncio.sleep(1)
    provider.go()

    await asyncio.sleep(1)
    assert consumer.consumed == [2]


def test_reducer_exists():
    with pytest.raises(
        ValueError,
        match='reducer<DataType.KLINE> already exists'
    ):
        Orchestrator([
            SimpleReducer(),
            SimpleReducer()
        ])


def test_connect_reducer_not_found():
    with pytest.raises(
        KeyError,
        match='reducer<DataType.KLINE,TimeSpan.DAY> must be defined'
    ):
        Orchestrator([]).connect(SimpleProvider())


def test_provider_exists():
    with pytest.raises(
        KeyError,
        match='provider<DataType.KLINE,TimeSpan.DAY> exists'
    ):
        Orchestrator([
            SimpleReducer()
        ]).connect(
            SimpleProvider()
        ).connect(
            SimpleProvider()
        )


def test_subscribe_provider_not_found():
    with pytest.raises(
        KeyError,
        match='provider<DataType.KLINE,TimeSpan.DAY> must be defined'
    ):
        Orchestrator([]).subscribe(
            SimpleConsumer()
        )


def test_dispatch_reducer_not_found():
    with pytest.raises(
        KeyError,
        match='reducer<DataType.KLINE,TimeSpan.DAY> is not found'
    ):
        Orchestrator([]).dispatch(
            vector,
            symbol,
            {}
        )
