"""
This file contains resource functions that access and manipulate user data
"""

from util.webshared import JSONResponse, Message, Error, secure
from collections import namedtuple

from bottle import request, response

from util.validation import validate_name, validate_username, validate_password

from data.db_models import User
from sqlalchemy.orm.exc import NoResultFound

from data.db_models import User


class Users(JSONResponse):

    def __init__(self, users):
        self.users = users

    @property
    def json(self):
        return {
            "users": [u.json for u in self.users]
        }


class UserJSON(JSONResponse):

    def __init__(self, user_id, username, first_name, last_name):
        self.id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def from_db(db_user):
        return UserJSON(db_user.id, db_user.username,
            db_user.first_name, db_user.last_name)


@secure()
def get_personal_info(db):
    # Needs user token
    # SELECT * FROM users WHERE id = token.userid
    return UserJSON.from_db(request.environ['user_info']).json


def create_new_user(db):
    try:
        data = request.json
        if data is None:
            raise ValueError

        if 'username' not in data or not validate_username(data['username']):
            raise ValueError
        if 'password' not in data or not validate_password(data['username']):
            raise ValueError
        if 'first_name' not in data or not validate_name(data['first_name']):
            raise ValueError
        if 'last_name' not in data or not validate_name(data['last_name']):
            raise ValueError

        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
    except ValueError:
        response.status = 400
        return Error("Missing JSON with valid username, password, " +
            "first_name, last_name").json

    count = db.query(User).filter(User.username == username).count()
    if count != 0:
        response.status = 400
        return Error("'%s' already exists" % username).json

    user = User(username=username, password_hash=password,
        first_name=first_name, last_name=last_name)
    db.add(user)
    db.commit()

    return UserJSON.from_db(user).json


@secure()
def change_personal_info(db):
    # Needs user token
    # Needs body info
    # UPDATE users SET user_info=new_info WHERE user_id = token.userid
    return Message("I have changed your personal info").json


@secure()
def delete_user(db):
    user = request.environ.get('user_info')
    if user is None:
        raise RuntimeError("delete_user should always have user_info")
    db.delete(user)
    return Message("I have deleted your user.  Why does everyone leave me?").json


def get_user_info(user_id, db):
    # Not authed?
    # SELECT * FROM users WHERE user.id = user_id
    try:
        user = db.query(User).get(user_id)
        return UserJSON.from_db(user).json
    except NoResultFound:
        response.status = 404
        return Error("User %d doesn't exist" % user_id).json


@secure()
def get_nearby_users(db):
    # Needs user token
    # url params to specify timeframe?
    # SELECT * FROM users WHERE ??????? << TABLE JOINS?
    return Users([UserJSON(1, "Bob"), UserJSON(2, "Anne")]).json
