import asyncio
import pandas as pd
import pathlib

from compton.quant.provider import Provider


# A fake provider to imitate the websocket messages
class MockProvider(Provider):
    def __init__(self, code, *args):
        super().__init__(*args)

        self._code = code
        self._to_be_updated = None

    def start(self):
        self._kline_future = asyncio.Future()
        self._done_future = asyncio.Future()

        self._task = asyncio.create_task(self._create_update_task())

    async def _create_update_task(self):
        while True:
            await asyncio.sleep(.01)

            if not self._to_be_updated:
                continue

            length = len(self._to_be_updated)

            if length == 1:
                update = self._to_be_updated
                break
            else:
                update = self._to_be_updated.iloc[0:1]
                self._to_be_updated = self._to_be_updated.iloc[1:]

            self._receive(self._code, 0, update)

        self._done_future.set_result()

    def set_receiver(self, _, receive):
        self._receive = receive

    async def kline(self):
        return await self._kline_future

    async def done(self):
        await self._done_future

    async def get_kline(self, *args):
        csv = pathlib.Path(__file__).parent / 'fixtures' / 'tencent.csv'
        kline = pd.read_csv(csv)

        self._kline_future.set_result(kline)

        self._to_be_updated = kline.iloc[50:]
        return kline.iloc[0: 50]

    async def subscribe(self, codes):
        return codes, [], {}
