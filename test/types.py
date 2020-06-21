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
    MAX = 3

    def __init__(self, i=0, update_delay=0):
        self._future = asyncio.Future()
        self._i = i
        self._discarded = set()
        self._dispatch = None
        self._update_delay = update_delay

    @property
    def vector(self):
        return vector

    async def init(self, symbol):
        asyncio.create_task(self._update())
        await self._future
        return dict(i=0)

    def remove(self, symbol):
        self._discarded.add(symbol)
        return

    def go(self):
        self._future.set_result(None)
        return self

    async def _update(self):
        if self._update_delay:
            await asyncio.sleep(self._update_delay)

        i = 1

        while i < self.MAX and symbol not in self._discarded:
            await asyncio.sleep(.05)
            self.dispatch(symbol, dict(i=i + self._i))
            i += 1


class SimpleProvider2(SimpleProvider):
    def __init__(self):
        super().__init__(1)

    @property
    def vector(self):
        return vector2


class SimpleProvider3(SimpleProvider):
    async def init(self, symbol):
        raise RuntimeError('you got me')


class SimpleProvider5(SimpleProvider):
    MAX = float('inf')


class SimpleReducer(Reducer):
    @property
    def vector(self):
        # It is a generic reducer for all kinds of klines
        return (DataType.KLINE,)

    def merge(self, old, new):
        if old is None:
            return new

        merged = {
            **old,
            **new
        }

        return merged


class SimpleReducer2(SimpleReducer):
    @property
    def vector(self):
        return (DataType.KLINE, TimeSpan.DAY)


class SimpleReducer3(SimpleReducer):
    def merge(self, *args):
        raise RuntimeError('you got me')


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

    @property
    def concurrency(self):
        return 1

    @property
    def all(self):
        return True

    def should_process(self, symbol, payload, payload2):
        return payload['i'] == payload2['i']

    async def process(self, symbol, payload, payload2):
        self.consumed.append(
            (
                None if payload is None else payload['i'],
                None if payload2 is None else payload2['i']
            )
        )


class SimpleConsumer4(SimpleConsumer2):
    @property
    def all(self):
        return False

    @property
    def concurrency(self):
        return 0

    def should_process(self, symbol, a, b):
        return a is not None and b is not None


class SimpleConsumer6(SimpleConsumer):
    def should_process(self, *args):
        raise RuntimeError('you got me')


class SimpleConsumer3(SimpleConsumer):
    async def process(self, symbol, payload):
        raise RuntimeError('you got me')


class SimpleConsumer5(SimpleConsumer2):
    def should_process(self, *args):
        return True

    @property
    def all(self):
        return False
