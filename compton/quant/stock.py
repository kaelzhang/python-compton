import logging

from stock_pandas import StockDataFrame
import pandas as pd

from futu import (
    CurKlineHandlerBase,
    RET_OK, RET_ERROR
)

from .provider import Provider


class StockManager:
    """The real entry of the application
    """

    def __init__(
        self,
        provider: Provider,
        strategy:
    ):
        self._stocks = {}
        self._provider = provider

        self._provider.set_handler(_, self._receive)

    def _receive(self, data):
        if not self._has(code):
            return

        self._stocks.get(code).receive(data)

    def _get_stock(self, code):
        stock = self._stocks.get(code, None)

        if stock:
            return stock, False



        return stock, True

    def _has(self, code):
        return code in self._stocks

    def add(self, code):
        if self._has(code):
            # stock already exists
            return False

        self._stocks[code] = Stock(code, self._context)

        # added
        return True

    def remove(self, code):
        if not self._has(code):
            # non-existing
            return False

        stock = self._stocks.get(code)
        stock.destroy()

        del self._stocks[code]
        # removed
        return True




TIME_KEY = 'time_key'

def make_time_key_datetime(target: pd.DataFrame) -> pd.DataFrame:
    target[TIME_KEY] = pd.to_datatime(target[TIME_KEY])
    return target


class Stock:
    def __init__(self, code, context):
        self._code = code
        self._context = context

        self._kline = None
        self._not_updated = None

    def destroy(self):
        self._code = None
        self._kline = None
        self._context = None



    def receive(self, update):
        kline_df = self._kline

        if not kline:
            self._not_updated = self._update_message(self._not_updated, update)
            return

        self._kline = self._update_message(self._kline, update)

    def _update_message(
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

        returnn target.append(
            make_time_key_datetime(update),
            ignore_index=True
        )
