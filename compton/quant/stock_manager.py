import asyncio
# import logging
from typing import (
    Tuple
)

from stock_pandas import StockDataFrame
import pandas as pd

from .provider import (
    Provider,
    TimeSpan,
    UpdateType
)


class StockManager:
    """The real entry of the application
    """

    def __init__(
        self,
        provider: Provider,
        # strategy
    ):
        self._stocks = {}
        self._provider = provider
        # self._strategy = strategy

        self._provider.set_handler(UpdateType.KLINE, self._receive)

    def _receive(
        self,
        code: str,
        update_type: int,
        data
    ):
        if not self._has(code):
            return

        self._stocks.get(code).receive(update_type, data)

    def _get_stock(self, code):
        stock = self._stocks.get(code, None)

        if stock:
            return stock

        stock = Stock(code, self._provider, self._strategy)
        self._stocks.set(code, stock)

        return stock

    def _has(self, code):
        return code in self._stocks

    def subscribe(self, codes) -> Tuple[list, list, dict]:
        subscribed = []
        already = []
        errored = {}

        for code in codes:
            if self._has(code):
                already.append(code)
                continue

            success, err_msg = self._provider.subscribe(code)

            if success:
                subscribed.append(code)
                self._stocks[code] = Stock(code, self._provider)
                continue
            else:
                errored[code] = err_msg

        return subscribed, already, errored

    # def remove(self, code):
    #     if not self._has(code):
    #         # non-existing
    #         return False

    #     stock = self._stocks.get(code)
    #     stock.destroy()

    #     del self._stocks[code]
    #     # removed
    #     return True


TIME_KEY = 'time_key'


def make_time_key_datetime(target: pd.DataFrame) -> pd.DataFrame:
    target[TIME_KEY] = pd.to_datatime(target[TIME_KEY])
    return target


class Stock:
    def __init__(self, code, provider):
        self._code = code
        self._provider = provider

        self._kline = None
        self._not_updated = None

        self._task = asyncio.create_task(self._fetch_kline())

    def destroy(self):
        self._code = None
        self._kline = None
        self._provider = None
        self._not_updated = None

    async def _fetch_kline(self):
        kline = self._provider.get_kline(self._code, TimeSpan.DAY, 100)
        self._kline = self._update_kline(None, kline)
        print(self._kline)

    def receive(self, _, update):
        if not self._kline:
            self._not_updated = self._update_kline(self._not_updated, update)
            return

        self._kline = self._update_kline(self._kline, update)
        print(self._kline)

    def _update_kline(
        self,
        target,
        update
    ) -> StockDataFrame:
        if target is None:
            return make_time_key_datetime(StockDataFrame(update))

        # For now, we don't use DateTimeIndex for
        # DateTimeIndex is really buggy that even we can't drop raws
        new_kline_time = update.iloc[0]

        duplicates = target[target[TIME_KEY] >= new_kline_time]

        if len(duplicates):
            target = target.drop(duplicates.index)

        return target.append(
            make_time_key_datetime(update),
            ignore_index=True
        )
