"""
This file contains resource functions that access and manipulate user data
"""

from util.webshared import JSONResponse, Message
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
    def __init__(self, name):
        self.name = name



def get_personal_info():
    # Needs user token
    # SELECT * FROM users WHERE id = token.userid
    return User("Harry").json

def create_new_user():
    # Not authed
    # Rate-limited?
    # INSERT INTO users VALUE (user_info)
    return Message("I have created a new user for you").json

def change_personal_info():
    # Needs user token
    # Needs body info
    # UPDATE users SET user_info=new_info WHERE user_id = token.userid
    return Message("I have changed your personal info").json

def delete_user():
    # Needs user token
    # DELETE FROM users WHERE user.id = token.userid
    return Message("I have deleted your user.  Why does everyone leave me?").json

def get_user_info(user_id):
    # Not authed?
    # SELECT * FROM users WHERE user.id = user_id
    return User("Bob").json

def get_nearby_users():
    # Needs user token
    # url params to specify timeframe?
    # SELECT * FROM users WHERE ??????? << TABLE JOINS?
    return Users([User("Bob"), User("Anne")]).json
