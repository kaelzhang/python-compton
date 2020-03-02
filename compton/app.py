from .server import Server
from .server.views import *
from .config import (
    SERVER_PORT,
    FUTU_HOST,
    FUTU_PORT
)

app = Server(dict(
    port=SERVER_PORT
))

@app.put('/subscribe')
async def subscribe(request):
    pass

start()
