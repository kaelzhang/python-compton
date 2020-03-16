import asyncio

from aiohttp import web
from aiohttp.web import middleware

from .exceptions import ResponseException

@middleware
async def response(request, handler):
    try:
        resp = await handler(request)
    except ResponseException as e:
        return web.json_response(dict(
            code = e.code,
            message = e.message
        ), status = e.status)
    else:
        return web.json_response(resp)

class Server:
    def __init__(self, port, routes):
        self._port = port

        app = web.Application(
            middlewares = [response]
        )
        app.add_routes(routes)

        self._app = app

    async def start(self):
        runner = web.AppRunner(self._app)
        await runner.setup()

        site = web.TCPSite(runner, 'localhost', self._port)
        await site.start()

        print(f'server started at localhost:{self._port}')

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        loop.run_forever()
