from abc import ABC, abstractmethod
from typing import (
    Optional,
    Tuple,
)

from .types import (
    Vector,
    Symbol,
    Payload
)

from .common import (
    get_hierachical
)


class Reducer(ABC):
    def __init__(self):
        self._not_updated = {}

    def __str__(self):
        return f'reducer{self.vector}'

    @property
    @abstractmethod
    def vector(self) -> Vector:
        """The vector of a reducer could be a more generic vector which is much
        shorter.

        Reducer::vector always does semi matching
        """

        return

    def reduce(
        self,
        previous: Payload,
        payload: Payload,
        symbol: Symbol,
        vector: Vector
    ) -> Tuple[bool, Optional[Payload]]:
        """Applies the update payload

        Args:
            previous (Payload):

        Returns:
            Tuple[bool, Optional[Payload]]:
            - the first item in the tuple indicates whether the data changes.
            - If no changes, the second item will be `None`
        """

        last = vector[-1]
        partial_vector = (symbol, vector[:-1])

        parent = get_hierachical(
            self._not_updated,
            partial_vector,
            {},
            True
        )

        not_updated = parent.get(last, None)

        if not previous:
            parent[last] = self.merge(
                not_updated,
                payload
            ) if not_updated else payload

            return False, None

        return True, self.merge(previous, not_updated)

    @abstractmethod
    def merge(
        self,
        target: Payload,
        payload: Payload
    ) -> Payload:
        pass
