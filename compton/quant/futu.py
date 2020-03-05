from futu import (
    OpenQuoteContext,
    SubType,
    RET_OK
)
# import matplotlib.pyplot as plt

from .stock import StockManager

class FutuContext:
    def __init__(self, host, port):
        ctx = OpenQuoteContext(host=host, port=port)
        self._ctx = ctx

        self._stock_manager = StockManager(ctx)

    def subscribe(self, codes):
        ret, err_message = self._ctx.subscribe(codes, [
            SubType.K_DAY,

            # SubType.QUOTE,
            # SubType.TICKER,
            # SubType.ORDER_BOOK,
            # SubType.RT_DATA,
            # SubType.BROKER
        ])

        if ret != RET_OK:
            return False, err_message

        self._stock_manager.add(codes)

        return True, None

    def unsubscribe(self, codes):
        ret, err_message = self._ctx.unsubscribe(codes, [
            SubType.K_DAY
        ])

        if ret != RET_OK:
            return False, err_message

        self._stock_manager.remove(codes)

        return True, None
