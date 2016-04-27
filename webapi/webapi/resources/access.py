from bottle import request, response
from util.validation import validate_username, validate_password
from util.webshared import JSONResponse, Message, Error, secure, TOKEN_VALUE
from data.db_models import Session, User

from datetime import datetime, timedelta
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

import uuid, OpenSSL

def generate_token(num_bytes=16):
    return str(uuid.UUID(bytes=OpenSSL.rand.bytes(16)))

class Token(JSONResponse):

    def __init__(self, token):
        self.token = token


def login(db):
    """
    Are there potential exploits in user JSON over form format?
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
        session = db.query(Session) \
            .filter(Session.user_id == user.id) \
            .one()
    except NoResultFound:
        while True:
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
    auth = request.headers.get('Authentication')
    if auth is None:
        raise RuntimeError("logout should always have Authentication header")
    try:
        session = db.query(Session).filter(Session.session_hash == auth).one()
    except NoResultFound:
        print("logout: Authentication token doesn't exist in db")
        response.status = 400
        return Error("Authentication token is invalid").json

    db.delete(session)

    return Message("You are now logged out!").json
