class ResponseException(Exception):
    def __init__(self, message, code=- 1, status=200):
        self.message = message
        self.code = code
        self.status = status
