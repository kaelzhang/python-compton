import asyncio
from concurrent.futures import ThreadPoolExecutor

from futu import (
    CurKlineHandlerBase,
    RET_OK, RET_ERROR
)

class StockManager:
    def __init__(self, context):
        self._stocks = {}
        self._context = context

        class KlineHandler(CurKlineHandlerBase):
            def on_recv_rsp(s, res):
                ret_code, data = super().on_recv_rsp(res)

                if ret_code != RET_OK:
                    # TODO: log
                    return RET_ERROR, data

                self._receive(data)

                return RET_OK, data

        context.set_handler(KlineHandler())

    def _receive(self, data):
        code = data['code'][0]
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

fetch_executor = ThreadPoolExecutor(
    max_workers = 5
)

class Stock:
    def __init__(self, code, context):
        self._code = code
        self._context = context

        self._kline = None

    def destroy(self):
        self._code = None
        self._kline = None
        self._context = None

    # This method is not a coroutine function,
    #   and will block
    def _fetch_kline(self):
        ret, kline = self._context.get_cur_kline(self._code, 100)

        if ret != RET_OK:
            # TODO: error handling
            return None

        return kline

    async def _fetch(self):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            fetch_executor,
            self._fetch_kline
        )

    def receive(self, data):
        pass
