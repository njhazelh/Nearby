from bottle import request, response
from util.request_validation import validate_username, validate_password
import json
from collections import namedtuple
from util.webshared import JSONResponse, Message, secure, TOKEN_VALUE


class Token(JSONResponse):

    def __init__(self, token):
        self.token = token


def login():
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
        print("ValueError")
        response.status = 400
        return

    # SELECT * FROM users WHERE user.username = username
    # check if password matches database using scrypt
    # Generate session token
    # INSERT INTO sessions VALUE (token, user_id, expiration)
    # Return token
    return Token(TOKEN_VALUE).json


@secure()
def logout():
    # Needs user token
    # DELETE FROM sessions WHERE session.id = token
    return Message("You are now logged out!").json
