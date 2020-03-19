import asyncio
import pytest

from compton import (
    Orchestrator,
    Provider,
    Reducer,
    Consumer,
    DataType,
    TimeSpan
)


symbol = 'US.TSLA'

vector = (DataType.KLINE, TimeSpan.DAY)


class SimpleProvider(Provider):
    @property
    def vector(self):
        return vector

    async def init(self, symbol):
        self._future = asyncio.Future()
        await self._future
        return dict(i=0)

    def go(self):
        self._future.set_result()

    async def _update(self, dispatch):
        i = 1

        while i < 3:
            await asyncio.sleep(.05)
            dispatch(symbol, dict(i=i))

    def when_update(self, dispatch):
        asyncio.create_task(self._update(dispatch))


class SimpleReducer(Reducer):
    @property
    def vector(self):
        # It is a generic reducer for all kinds of klines
        return (DataType.KLINE,)

    def merge(self, old, new):
        return old.update(new)


class SimpleConsumer(Consumer):
    def __init__(self):
        self.consumed = []

    @property
    def vectors(self):
        return [vector]

    async def process(self, symbol, payload):
        self.consumed.append(dict(
            symbol=symbol,
            payload=payload
        ))


@pytest.mark.asyncio
async def test_main():
    consumer = SimpleConsumer()
    provider = SimpleProvider()

    Orchestrator(
        [SimpleReducer()]
    ).connect(
        SimpleProvider()
    ).subscribe(
        consumer
    ).add(symbol)

    await asyncio.sleep(.2)
    provider.go()

    await asyncio.sleep(.1)
    print(consumer.consumed)
