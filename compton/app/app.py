from compton.server import Server
from .config import SERVER_PORT
from .routes import routes

app = Server(port=SERVER_PORT, routes=routes)
