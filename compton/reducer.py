from abc import ABC, abstractmethod
# from typing import (
#     Optional,
#     Tuple,
# )

from .types import (
    Vector,
    Symbol,
    Payload
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
        shorter
        """

        return

    @abstractmethod
    def reduce(
        self,
        previous: Payload,
        payload: Payload,
        symbol: Symbol,
        vector: Vector
    ):
        pass
