class JSONResponse:
    @property
    def json(self):
        return self.__dict__


class Message(JSONResponse):
    def __init__(self, message):
        self.message = message
