from typing import (
    Callable,
    Tuple,
    Optional,
    List
)

from pandas import DataFrame

from futu import (
    OpenQuoteContext,
    SubType,
    RET_OK
)


class UpdateType:
    KLINE = 1


class TimeSpan:
    DAY = 1


class Provider:
    """Provide is used to get the latest data remotely
    """

    async def get_kline(
        self,
        code: str,
        span: int,
        limit: int
    ) -> Optional[DataFrame]:
        """Gets the kline dataframe
        """

        raise NotImplementedError

    def set_receiver(
        receiver_type: int,
        receiver: Callable
    ) -> None:
        """Sets the receiver to receive update messages
        """

        raise NotImplementedError

    def subscribe(
        self,
        codes: List[str]
    ) -> Tuple[bool, Optional[str]]:
        """Subscribe to the provider.

        This method could do nothing.
        """

        raise NotImplementedError

    def unsubscribe(
        self,
        codes: List[str]
    ) -> Tuple[bool, Optional[str]]:
        raise NotImplementedError
