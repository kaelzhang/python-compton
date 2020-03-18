from abc import ABC, abstractmethod
from typing import (
    Callable,
    Optional
)

from pandas import DataFrame

from .types import (
    Vector,
    Symbol,
    Payload
)


class Provider(ABC):
    """
    """

    def __str__(self):
        return f'provider{self.vector}'

    @property
    @abstractmethod
    def vector(self) -> Vector:
        """A provider should only have one vector
        which means a provider should only handle a single type of message
        """

        return

    @abstractmethod
    async def init(
        self,
        symbol: Symbol
    ) -> Optional[DataFrame]:
        """Initialize the data from the very beginning
        """

        return

    @abstractmethod
    def update(
        dispatch: Callable[Symbol, Payload]
    ) -> None:
        """Sets the receiver to receive update messages
        """

        return

    # def subscribe(
    #     self,
    #     codes: List[str]
    # ) -> Tuple[bool, Optional[str]]:
    #     """Subscribe to the provider.

    #     This method could do nothing.
    #     """

    #     raise NotImplementedError

    # def unsubscribe(
    #     self,
    #     codes: List[str]
    # ) -> Tuple[bool, Optional[str]]:
    #     raise NotImplementedError
