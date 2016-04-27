from bottle import request, response
from util.validation import validate_username, validate_password
from util.webshared import JSONResponse, Message, Error, secure
from data.db_models import Session, User

from datetime import datetime, timedelta
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

import uuid, OpenSSL

def generate_token(num_bytes=16):
    """
    Generate a unique token string (default 128-bit).

    :param num_bytes: The number of random bytes to generate
    :returns: A string with num_bytes of cryptographically secure random data.
    """
    return str(uuid.UUID(bytes=OpenSSL.rand.bytes(16)))

class Token(JSONResponse):
    """
    An object to encapsulate the token in JSON.
    """
    def __init__(self, token):
        self.token = token


def login(db):
    """
    Generate a session with the server.

    Session generation performed according to the following steps.
    1. Client presents username and password
    2. Server authenticates username and password.
    3. Server generates cryptographically secure random token if session doesn't
        already exist and send to client.
    4. Server sends previously generated random token if session already exists.

    This session token must be provided with each future request in an HTTP
    header called 'Authentication'.

    Login request must contain JSON body:

    {
        "username": <string>,
        "password": <string>,
    }

    :param db: The database session
    :returns: Error JSON on fail or Session token JSON on success.
    """
    try:
        data = request.json

        if data is None:
            raise ValueError

        # validate data
        if 'username' not in data or not validate_username(data['username']):
            raise ValueError
        if 'password' not in data or not validate_password(data['password']):
            raise ValueError

        username = data['username']
        password = data['password']
    except ValueError:
        response.status = 400
        return Error("Missing valid username or password").json

    # Verify username/password combo with database
    try:
        user = db.query(User) \
            .filter(User.username == username, User.password_hash == password) \
            .one()
    except NoResultFound:
        response.status = 401
        return Error("Username/Password combo is invalid").json
    except MultipleResultsFound:
        response.status = 500
        return Error("Somehow multiple users exist with that username/password")

    try:
        # Try to revieve old session token
        session = db.query(Session) \
            .filter(Session.user_id == user.id) \
            .one()
    except NoResultFound:
        # No previous session so generate new token
        while True:
            # Make sure session token doesn't already exist.
            token = generate_token()
            if db.query(Session) \
                 .filter(Session.session_hash == token).count() == 0:
                break
        session = Session(
            session_hash=token, user_id=user.id,
            expires=datetime.now() + timedelta(weeks=2))
        db.add(session)

    return Token(session.session_hash).json


@secure()
def logout(db):
    """
    Remove the current session token from database.

    :param db: The database session
    :returns: Error JSON on fail, Message JSON on success.
    """
    # Get session token
    auth = request.headers.get('Authentication')
    if auth is None:
        raise RuntimeError("logout should always have Authentication header")

    # Try to find the session token
    try:
        session = db.query(Session).filter(Session.session_hash == auth).one()
    except NoResultFound:
        print("logout: Authentication token doesn't exist in db")
        response.status = 400
        return Error("Authentication token is invalid").json

    # Delete the session
    db.delete(session)
    d.commit()

    return Message("You are now logged out!").json
