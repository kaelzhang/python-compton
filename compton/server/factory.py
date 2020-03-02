from aiohttp import web

class Server:
    def __init__(self, config):
        self._app = web.Application()
        self._config = config

    def _create_add_route(self, method, path):
        def decorator(handler):
            getattr(self._app.router, method)(path, handler)

        return decorator

    def get(path):
        return self._create_add_route('add_get', path)

    def post(path):
        return self._create_add_route('add_post', path)

    def put(path):
        return self._create_add_route('add_put', path)

    def delete(path):
        return self._create_add_route('add_delete', path)

    def start(self):
        self._app['config'] = self._config
        web.run_app(self._app)
