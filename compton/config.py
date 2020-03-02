import os

env = os.environ

SERVER_PORT = int(env.get('SERVER_PORT', '80'))
FUTU_HOST = env.get('FUTU_HOST', 'localhost')
FUTU_PORT = int(env.get('FUTU_PORT', 11111))
