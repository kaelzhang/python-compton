from typing import (
    List
)

from .provider import Provider
from .consumer import Consumer
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


class Orchestrator:
    """
    """

    def __init__(
        self,
        reducers: List[Reducer]
    ):
        self._store = {}
        self._providers = {}
        self._subscribed = {}

        saved_reducers = {}

        for reducer in reducers:
            vector = get_vector(reducer)

            # We set hierachically for reducers, because
            # we allow reducers to do a semi matching
            success, context = set_hierachical(saved_reducers, vector, reducer)

            if not success:
                raise ValueError(
                    f'a reducer{stringify_vector(context)} already exists'
                )

        self._reducers = saved_reducers

    def connect(
        self,
        provider: Provider
    ) -> None:
        """Connect to a provider
        """

        vector = get_vector(provider)
        reducer = get_hierachical(self._saved_reducers, vector)

        if reducer is None:
            raise KeyError(
                f'a reducer{vector} must be defined before connecting to {provider}'  # noqa:E501
            )

        self._providers[vector] = provider

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

            self._subscribed[vector] = consumer

            if vector not in self._providers:
                raise KeyError(f'a provider{vector} must be defined before subscription')  # noqa:E501

            if vector not in self._subscribed:
                consumers = []
                self._subscribed[vector] = consumers
            else:
                consumers = self._subscribed[vector]

            consumers.append(consumer)

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




    def add(
        self,
        symbol: Symbol
    ) -> bool:
        """Adds a new stock symbol to the orchestrator
        """

        pass
