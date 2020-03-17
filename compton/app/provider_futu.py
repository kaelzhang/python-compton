import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

from futu import (
    OpenQuoteContext,
    CurKlineHandlerBase,
    SubType,
    RET_OK, RET_ERROR
)

from compton.quant.provider import (
    Provider,
    UpdateType,
    # TimeSpan
)


logger = logging.getLogger(__name__)


class FutuProvider(Provider):
    EXECUTOR_MAX_WORKERS = 5

    def __init__(self, host, port):
        ctx = OpenQuoteContext(host=host, port=port)

        self._ctx = ctx
        self._fetch_executor = ThreadPoolExecutor(
            max_workers=self.EXECUTOR_MAX_WORKERS
        )

    # This method is not a coroutine function,
    #   and will block
    def _fetch_kline(self, code, _, limit):
        ret, kline = self._ctx.get_cur_kline(self._code, limit)

        if ret != RET_OK:
            logger.error('fails to fetch kline for stock %s', self._code)
            return None

        return kline

    # TODO: get kline for other timespan than DAY
    async def get_kline(self, code, _, limit):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._fetch_executor,
            self._fetch_kline, code, _, limit
        )

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

    def set_receiver(self, _, receive):
        class KlineHandler(CurKlineHandlerBase):
            def on_recv_rsp(s, res):
                ret_code, data = super().on_recv_rsp(res)

                if ret_code != RET_OK:
                    return RET_ERROR, data

                code = res['code'][0]

                receive(code, UpdateType.KLINE, data)

                return RET_OK, data

        self._ctx.set_handler(KlineHandler())
