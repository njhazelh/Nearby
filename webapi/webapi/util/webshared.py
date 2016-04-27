from bottle import request, response
from data.db_models import Session, User
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


class JSONResponse:
    """
    A Base class to be extended by other classes.

    Provides basic functionality for converting object field values info
    JSON key/value pairs.

    The json property of this object returns a dict.  The application relies on
    bottle's JSON plugin to convert all dictionaries to JSON and set the
    Content-Type of the response to application/json.
    """

    @property
    def json(self):
        # Get the dictionary of field/value pairs for the object
        d = self.__dict__

        # Convert lists of JSON objects to lists of dictionaries
        for key in d.keys():
            if isinstance(d[key], list):
                d[key] = [x.json for x in d[key]]

        return d


class Message(JSONResponse):
    """
    An object to contain Message information as JSON
    """

    def __init__(self, message):
        self.message = message


class Error(JSONResponse):
    """
    An object to contain Error information as JSON
    """

    def __init__(self, error):
        self.error = error


class secure:
    """
    This class is decorator for resource functions.
    By applying it, all requests that would have gone directly to the resource
    go to __call__ instead.

    Here the requests is authenticated by checking the Authentication
    header on the request for a valid session token.  These session tokens
    are available via POSTing to /api/access with a username and password.
    """

    def __init__(self, level="logged_in"):
        self.level = level

    def __call__(self, resource):
        def decorator(**kwargs):
            """
            decorator function to check validity of session tokens and
            store user info in request environment.

            :param **kwargs: The arguments to the resource. Must contain
                database session object as 'db'
            :returns: Error JSON if auth fails, else response from resource.
            """
            print("Authentication Check: level '%s'" % self.level)

            # Access the database session
            db = kwargs['db']

            # Access the session token
            auth = request.headers.get("Authentication")
            if auth is None:
                print("Missing authentication token")
                response.status = 401
                return Error("Missing authentication token").json

            # Lookup the session token in the database
            try:
                session = db.query(Session) \
                    .filter(Session.session_hash == auth) \
                    .one()
            except NoResultFound:
                print("Authentication token invalid")
                response.status = 401
                return Error("Authentication token is invalid").json

            print("Authentication check passes")

            # Store information of user in request environment
            request.environ['user_info'] = session.user

            # Return response from resource
            return resource(**kwargs)
        return decorator
