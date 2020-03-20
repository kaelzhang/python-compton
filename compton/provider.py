from abc import ABC, abstractmethod
from typing import (
    Callable,
    Optional
)

from pandas import DataFrame

from .common import (
    stringify_vector,

    Vector,
    Symbol,
    Payload
)


class Provider(ABC):
    """
    """

    @staticmethod
    def check(provider):
        if not isinstance(provider, Provider):
            raise ValueError(
                f'provider must be an instance of Provider, but got `{provider}`'  # noqa: E501
            )

    def __str__(self):
        return f'provider{stringify_vector(self.vector)}'

    @property
    @abstractmethod
    def vector(self) -> Vector:  # pragma: no cover
        """A provider should only have one vector
        which means a provider should only handle a single type of message
        """

        return

    @abstractmethod
    async def init(
        self,
        symbol: Symbol
    ) -> Optional[DataFrame]:  # pragma: no cover
        """Initialize the data from the very beginning
        """

        return

    @abstractmethod
    def when_update(
        dispatch: Callable[[Symbol, Payload], None]
    ) -> None:  # pragma: no cover
        """Sets the receiver to receive update messages
        """

        return
