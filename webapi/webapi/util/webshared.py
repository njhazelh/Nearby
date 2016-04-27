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

    def __init__(self, error):
        self.error = error


class secure:
    """
    This class is decorator for resource functions.  By applying it,
    all requests that would have gone directly to the resource go to __call__
    instead.  Here the requests is authenticated by checking the Authentication
    header on the request for a valid session token.  These session tokens
    are available via POSTing to /api/access with a username and password.
    """

    def __init__(self, level="logged_in"):
        self.level = level

    def __call__(self, resource):
        def decorator(**kwargs):
            print("Authentication Check: level '%s'" % self.level)
            auth = request.headers.get("Authentication")
            if auth is None:
                print("Missing authentication token")
                response.status = 401
                return Error("Missing authentication token").json
            if auth != TOKEN_VALUE:
                print("Authentication token invalid")
                response.status = 401
                return Error("Authentication token is invalid").json
            print("Authentication check passes")

            # TODO: Lookup user information from TokenValue

            return resource(**kwargs)
        return decorator
