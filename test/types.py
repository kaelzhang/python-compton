import asyncio
from compton import (
    Provider,
    Reducer,
    Consumer
)


from enum import Enum


class DataType(Enum):
    KLINE = 1


class TimeSpan(Enum):
    DAY = 1


symbol = 'US.TSLA'

vector = (DataType.KLINE, TimeSpan.DAY)


class SimpleProvider(Provider):
    def __init__(self):
        self._future = asyncio.Future()

    @property
    def vector(self):
        return vector

    async def init(self, symbol):
        await self._future
        return dict(i=0)

    def go(self):
        self._future.set_result(None)
        return self

    async def _update(self, dispatch):
        i = 1

        while i < 3:
            await asyncio.sleep(.05)
            dispatch(symbol, dict(i=i))
            i += 1

    def when_update(self, dispatch):
        asyncio.create_task(self._update(dispatch))


class SimpleReducer(Reducer):
    @property
    def vector(self):
        # It is a generic reducer for all kinds of klines
        return (DataType.KLINE,)

    def merge(self, old, new):
        merged = {
            **old,
            **new
        }

        return merged


class SimpleConsumer(Consumer):
    def __init__(self):
        self.consumed = []

    @property
    def vectors(self):
        return [vector]

    async def process(self, symbol, payload):
        self.consumed.append(payload['i'])
