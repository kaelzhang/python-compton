from futu import (
    OpenQuoteContext,
    SubType,
    RET_OK
)
# import matplotlib.pyplot as plt

class FutuContext:
    def __init__(self, host, port):
        self._ctx = OpenQuoteContext(host=host, port=port)

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

        return True, None

    def unsubscribe(self, codes):
        ret, err_message = self._ctx.unsubscribe(codes, [
            SubType.K_DAY
        ])

        if ret != RET_OK:
            return False, err_message

        return True, None

