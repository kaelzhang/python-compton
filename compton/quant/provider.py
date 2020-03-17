from typing import (
    Callable,
    Tuple,
    Optional,
    List
)

from pandas import DataFrame


class ProviderType:
    KLINE = 1


class UpdateType:
    KLINE = 1


class TimeSpan:
    DAY = 1


class Provider:
    """Provide is used to get the latest data remotely

    A provide should:
    - handle different stock codes
    -
    """

    async def init(
        self,
        code: str,
        *args
    ) -> Optional[DataFrame]:
        """Initialize the data from the very beginning
        """

        raise NotImplementedError

    def set_receiver(
        receiver_type: int,
        receiver: Callable
    ) -> None:
        """Sets the receiver to receive update messages
        """

        raise NotImplementedError

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
