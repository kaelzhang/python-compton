from aiohttp import web

from compton.server.exceptions import ResponseException

routes = web.RouteTableDef()


def create_err_msg(errored):
    for code, msg in enumerate(errored):
        return f'fails to subscribe {code}: {msg}'


@routes.post('/subscribe')
async def subscribe(request):
    body = await request.json()
    code_list = body.get('code_list', [])

    if not code_list:
        raise ResponseException('code_list is empty or not specified')

    stock = request.app['stock_manager']
    subscribed, already, errored = stock.subscribe(code_list)

    if errored:
        err_msg = create_err_msg(errored)
        raise ResponseException(err_msg)

    return dict(
        subscribed=subscribed,
        already=already,
        errored=errored
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
