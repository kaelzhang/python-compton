from aiohttp import web

from .server import ResponseException
from .config import (
    FUTU_HOST,
    FUTU_PORT
)

routes = web.RouteTableDef()

@routes.post('/subscribe')
async def subscribe(request):
    body = await request.json()
    code_list = body.get('code_list', [])

    if not code_list:
        raise ResponseException('code_list is empty or not specified')

    ok, err_msg = futu.subscribe(code_list)

    if not ok:
        raise ResponseException(err_msg)

    return dict(
        subscribed = code_list
    )

@routes.delete('/subscribe')
async def unsubscribe(request):
    body = await request.json()
    code_list = body.get('code_list', [])

    if not code_list:
        raise ResponseException('code_list is empty or not specified')

    ok, msg = futu.unsubscribe(code_list)

    if not ok:
        raise ResponseException(err_msg)

    return dict(
        unsubscribed = code_list
    )
