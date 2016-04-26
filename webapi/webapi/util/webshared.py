from bottle import request, response


TOKEN_VALUE = "some_magical_unique_token_thing"


class JSONResponse:

    @property
    def json(self):
        return self.__dict__


class Message(JSONResponse):

    def __init__(self, message):
        self.message = message


class Error(JSONResponse):

    def __init__(self, message):
        self.message = message


class secure:

    def __init__(self, level="logged_in"):
        self.level = level

    def __call__(self, resource):
        def decorator(**kwargs):
            auth = request.headers.get("Authentication")
            if auth is None:
                response.status = 401
                print("missing authentication token")
                return Error("Missing authentication token").json
            if auth != TOKEN_VALUE:
                response.status = 403
                print("authentication token invalid")
                return Error("Authentication token is invalid").json
            print("auth checked for: %s" % self.level)
            val = resource(*kwargs)
            print("exit func")
            return val
        return decorator
