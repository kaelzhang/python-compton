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
    WEEK = 2


symbol = 'US.TSLA'

vector = (DataType.KLINE, TimeSpan.DAY)
vector2 = (DataType.KLINE, TimeSpan.WEEK)


class SimpleProvider(Provider):
    def __init__(self, i=0):
        self._future = asyncio.Future()
        self._i = i

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
            dispatch(symbol, dict(i=i + self._i))
            i += 1

    def when_update(self, dispatch):
        asyncio.create_task(self._update(dispatch))


class SimpleProvider2(SimpleProvider):
    def __init__(self):
        super().__init__(1)

    @property
    def vector(self):
        return vector2


class SimpleProvider3(SimpleProvider):
    async def init(self, symbol):
        raise RuntimeError('you got me')


class SimpleProvider4(SimpleProvider):
    def when_update(self, dispatch):
        raise RuntimeError('you got me')


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


class SimpleReducer2(SimpleReducer):
    @property
    def vector(self):
        return (DataType.KLINE, TimeSpan.DAY)


class SimpleConsumer(Consumer):
    def __init__(self):
        self.consumed = []

    @property
    def vectors(self):
        return [vector]

    async def process(self, symbol, payload):
        self.consumed.append(payload['i'])


class SimpleConsumer2(Consumer):
    def __init__(self):
        self.consumed = []

    @property
    def vectors(self):
        return [vector, vector2]

    def should_process(self, symbol, payload, payload2):
        return payload['i'] == payload2['i']

    async def process(self, symbol, payload, payload2):
        self.consumed.append((payload['i'], payload2['i']))


class SimpleConsumer3(SimpleConsumer):
    async def process(self, symbol, payload):
        raise RuntimeError('you got me')
