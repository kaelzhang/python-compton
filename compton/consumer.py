import asyncio
import logging
from abc import ABC, abstractmethod
from typing import (
    List
)

from .common import (
    check_vector,
    stringify_vector,

    Payload,
    Vector
)


class Consumer(ABC):
    @staticmethod
    def check(consumer):
        if not isinstance(consumer, Consumer):
            raise ValueError(
                f'consumer must be an instance of Consumer, but got `{consumer}`'  # noqa: E501
            )

        for vector in consumer.vectors:
            check_vector(vector, consumer)

    def __str__(self):
        try:
            vectors = stringify_vector([
                stringify_vector(vector)
                for vector in self.vectors
            ])
        except Exception:
            return 'consumer<invalid>'

        return f'consumer{vectors}'

    @property
    @abstractmethod
    def vectors(self) -> List[Vector]:  # pragma: no cover
        return

    def should_process(self, symbol, *args) -> bool:
        return True

    @abstractmethod
    async def process(self, symbol, *args):  # pragma: no cover
        pass


logger = logging.getLogger(__name__)


class ConsumerSentinel:
    def __init__(
        self,
        consumer: Consumer
    ):
        Consumer.check(consumer)

        self._consumer = consumer
        self._vectors = set(consumer.vectors)

        self._changed = {}
        self._processing = False

    @property
    def vectors(self):
        return self._consumer.vectors

    def satisfy(self, symbol, vector) -> bool:
        if symbol in self._changed:
            changed = self._changed[symbol]
        else:
            changed = set()
            self._changed[symbol] = changed

        changed.add(vector)

        # For do not allow simultaneously processing
        return changed == self._vectors and not self._processing

    def process(self, symbol, payloads: List[Payload]):
        if not self._consumer.should_process(symbol, *payloads):
            return

        # Only if we start to process, then we clear changed
        self._changed[symbol].clear()
        self._processing = True

        asyncio.create_task(self._process(symbol, payloads))

    async def _process(self, symbol, payloads):
        try:
            await self._consumer.process(symbol, *payloads)
        except Exception as e:
            logger.error('consumer process error: %s', e)

        self._processing = False
