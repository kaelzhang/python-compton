import asyncio
import pytest

from compton import (
    Orchestrator
)

from .types import (
    SimpleProvider,
    SimpleProvider2,
    SimpleReducer,
    SimpleReducer2,
    SimpleConsumer,
    SimpleConsumer2,
    symbol,
    vector,

    DataType
)


@pytest.mark.asyncio
async def test_main():
    consumer = SimpleConsumer()
    consumer2 = SimpleConsumer2()
    provider = SimpleProvider().go()
    provider2 = SimpleProvider2().go()

    Orchestrator(
        [SimpleReducer()]
    ).connect(
        provider
    ).connect(
        provider2
    ).subscribe(
        consumer
    ).subscribe(
        consumer2
    ).add(symbol)

    await asyncio.sleep(1)

    assert consumer.consumed == [0, 1, 2]
    assert consumer2.consumed == [
        (0, 0), (2, 2)
    ]


@pytest.mark.asyncio
async def test_main_with_no_subscription():
    consumer = SimpleConsumer()
    provider = SimpleProvider()

    o = Orchestrator(
        [SimpleReducer()]
    ).connect(
        provider
    ).add(symbol)

    await asyncio.sleep(1)
    provider.go()

    await asyncio.sleep(1)

    o.subscribe(consumer)

    assert not consumer.consumed


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


def test_reducer_another_generic_exists():
    with pytest.raises(
        ValueError,
        match='reducer<DataType.KLINE> already exists'
    ):
        Orchestrator([
            SimpleReducer(),
            SimpleReducer2()
        ])


def test_connect_reducer_not_found():
    with pytest.raises(
        KeyError,
        match='reducer<DataType.KLINE,TimeSpan.DAY> must be defined'
    ):
        Orchestrator([]).connect(SimpleProvider())


def test_provider_exists():
    class MoreGenericProvider(SimpleProvider):
        @property
        def vector(self):
            return (DataType.KLINE,)

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

    with pytest.raises(
        KeyError,
        match='provider<DataType.KLINE> exists'
    ):
        Orchestrator([
            SimpleReducer()
        ]).connect(
            MoreGenericProvider()
        ).connect(
            SimpleProvider()
        )

    with pytest.raises(
        KeyError,
        match='provider<DataType.KLINE,TimeSpan.DAY> exists'
    ):
        Orchestrator([
            SimpleReducer()
        ]).connect(
            SimpleProvider()
        ).connect(
            MoreGenericProvider()
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
