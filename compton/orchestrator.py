import asyncio
import logging
from functools import partial
from typing import (
    List
)

from .provider import Provider
from .consumer import (
    Consumer,
    ConsumerSentinel
)

from .reducer import Reducer
from .types import (
    Vector,
    Symbol,
    Payload
)

from .common import (
    get_vector,
    is_hashable,
    stringify_vector,
    set_hierachical,
    get_hierachical
)


logger = logging.getLogger(__name__)


class Orchestrator:
    """
    """

    MAX_INIT_RETRIES = 3

    def __init__(
        self,
        reducers: List[Reducer]
    ):
        self._store = {}
        self._providers = {}
        self._subscribed = {}
        self._reducers = {}

        self._apply_reducers(reducers)

    def _apply_reducers(self, reducers):
        saved_reducers = self._reducers

        for reducer in reducers:
            Reducer.check(reducer)

            vector = get_vector(reducer)

            # We set hierachically for reducers, because
            # we allow reducers to do a semi matching
            success, context = set_hierachical(saved_reducers, vector, reducer)

            if not success:
                raise ValueError(
                    f'a reducer{stringify_vector(context)} already exists'
                )

    def connect(
        self,
        provider: Provider
    ) -> None:
        """Connect to a provider
        """

        Provider.check(provider)

        vector = get_vector(provider)
        reducer = get_hierachical(self._saved_reducers, vector)

        if reducer is None:
            raise KeyError(
                f'a reducer{vector} must be defined before connecting to {provider}'  # noqa:E501
            )

        self._providers[vector] = provider

        return self

    def subscribe(
        self,
        consumer: Consumer
    ) -> None:
        """Let the consumer subscribe to the changes of the store
        """

        vectors = consumer.vectors

        for vector in vectors:
            if not is_hashable(vector):
                raise ValueError(f'{vector} is not hashable')

            if vector not in self._providers:
                raise KeyError(f'a provider{vector} must be defined before subscribing to {vector}')  # noqa:E501

            if vector not in self._subscribed:
                consumers = []
                self._subscribed[vector] = consumers
            else:
                consumers = self._subscribed[vector]

            consumers.append(ConsumerSentinel(consumer))

        return self

    def dispatch(
        self,
        symbol: Symbol,
        vector: Vector,
        payload: Payload
    ):
        """Dispatch updates to a certain vector.
        This method is mainly used for testing purpose
        """

        reducer = get_hierachical(self._reducers, vector)

        if reducer is None:
            raise KeyError(
                f'can not process dispatched payload, reason: reducer{vector} is not found'  # noqa:E501
            )

        store_vector = (symbol, vector)
        previous = get_hierachical(self._store, store_vector)
        changed, new = reducer.reduce(previous, payload, symbol, vector)

        if changed:
            self._set_store(symbol, vector, new)

    def _set_store(self, symbol, vector, payload):
        set_hierachical(self._store, (symbol, vector), payload)
        self._emit(symbol, vector)

    def _emit(self, symbol, vector):
        subscribed = self._subscribed.get(vector, None)

        if not subscribed:
            return

        for consumer_sentinel in subscribed:
            satisfied = consumer_sentinel.satisfy(vector)
            if not satisfied:
                continue

            consumer_sentinel.process(
                symbol,
                self._get_payloads_by_vectors(
                    symbol,
                    consumer_sentinel.vectors
                )
            )

    def _get_payloads_by_vectors(self, symbol, vectors):
        store = self._store[symbol]
        return [store.get(vector) for vector in vectors]

    def add(
        self,
        symbol: Symbol
    ) -> bool:
        """Adds a new stock symbol to the orchestrator
        """

        self._changed[symbol] = set()

        asyncio.create_task(self._start_providers(symbol))

    async def _start_providers(self, symbol: Symbol):
        tasks = []

        for vector, provider in enumerate(self._providers):
            dispatch = self.dispatch(vector=vector)
            provider.when_update(dispatch)

            tasks.append(self._start_provider(symbol, provider))

        await asyncio.wait(tasks)

    async def _start_provider(
        self,
        symbol,
        provider: Provider,
        retries: int = 0
    ):
        try:
            payload = await provider.init(symbol)
        except Exception as e:
            logger.error('init for symbol "%s" failed: %s', symbol, e)

            if retries < self.MAX_INIT_RETRIES:
                return self._start_provider(symbol, provider, retries + 1)

            logger.error('give up init symbol "%s"', symbol)

        self._set_store(symbol, provider.vector, payload)
