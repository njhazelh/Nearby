"""
This file contains resource functions that access and manipulate user data
"""

from util.webshared import JSONResponse, Message, secure
from collections import namedtuple


class Users(JSONResponse):

    def __init__(self, users):
        self.users = users

    @property
    def json(self):
        return {
            "users": [u.json for u in self.users]
        }


class User(JSONResponse):

    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name


@secure()
def get_personal_info():
    # Needs user token
    # SELECT * FROM users WHERE id = token.userid
    return User(1, "Harry").json


def create_new_user():
    # Not authed
    # Rate-limited?
    # INSERT INTO users VALUE (user_info)
    return Message("I have created a new user for you").json


@secure()
def change_personal_info():
    # Needs user token
    # Needs body info
    # UPDATE users SET user_info=new_info WHERE user_id = token.userid
    return Message("I have changed your personal info").json


@secure()
def delete_user():
    # Needs user token
    # DELETE FROM users WHERE user.id = token.userid
    return Message("I have deleted your user.  Why does everyone leave me?").json


def get_user_info(user_id):
    # Not authed?
    # SELECT * FROM users WHERE user.id = user_id
    return User(1, "Bob %d" % user_id).json


@secure()
def get_nearby_users():
    # Needs user token
    # url params to specify timeframe?
    # SELECT * FROM users WHERE ??????? << TABLE JOINS?
    return Users([User(1, "Bob"), User(2, "Anne")]).json
