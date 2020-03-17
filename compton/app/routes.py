from aiohttp import web

from compton.server import ResponseException
from .config import (
    FUTU_HOST,
    FUTU_PORT
)
from .provider_futu import FutuProvider
from compton.quant.stock_manager import StockManager

provider = FutuProvider(FUTU_HOST, FUTU_PORT)
stock = StockManager(provider)

routes = web.RouteTableDef()

@routes.post('/subscribe')
async def subscribe(request):
    body = await request.json()
    code_list = body.get('code_list', [])

    if not code_list:
        raise ResponseException('code_list is empty or not specified')

    subscribed, already, errored = stock.subscribe(code_list)

    if not ok:
        raise ResponseException(err_msg)

    return dict(
        subscribed = subscribed,
        already = already,
        errored = errored
    )

# @routes.delete('/subscribe')
# async def unsubscribe(request):
#     body = await request.json()
#     code_list = body.get('code_list', [])

#     if not code_list:
#         raise ResponseException('code_list is empty or not specified')

#     ok, msg = futu.unsubscribe(code_list)

#     if not ok:
#         raise ResponseException(err_msg)

#     return dict(
#         unsubscribed = code_list
#     )
