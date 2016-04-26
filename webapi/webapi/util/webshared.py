class JSONResponse:
    @property
    def json(self):
        return self.__dict__


class Message(JSONResponse):
    def __init__(self, message):
        self.message = message

class secure:
    def __init__(self, level="logged_in"):
        self.level = level

    def __call__(self, resource):
        def decorator():
            print("auth checked: %s" % self.level)
            val = resource()
            print("exit func")
            return val
        return decorator
