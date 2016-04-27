"""
This file contains resource functions that access and manipulate user data
"""

from util.webshared import JSONResponse, Message, Error, secure
from collections import namedtuple

from bottle import request, response

from util.validation import validate_name, validate_username, validate_password

from data.db_models import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import text

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
    user = request.environ.get('user_info')
    if user is None:
        raise RuntimeError('change_personal_info should always have user_info')

    data = request.json
    if data is None:
        return UserJSON.from_db(user).json

    try:
        if 'username' in data and not validate_username(data['username']):
            raise ValueError
        if 'password' in data and not validate_password(data['username']):
            raise ValueError
        if 'first_name' in data and not validate_name(data['first_name']):
            raise ValueError
        if 'last_name' in data and not validate_name(data['last_name']):
            raise ValueError
    except ValueError:
        response.status = 400
        return Error("Update contains invalid data").json


    username = data.get('username', user.username)
    password = data.get('password', user.password_hash)
    first_name = data.get('first_name', user.first_name)
    last_name = data.get('last_name', user.last_name)

    if username != user.username:
        count = db.query(User).filter(User.username == username).count()
        if count != 0:
            response.status = 400
            return Error("'%s' already exists" % username).json

    user.username = username
    user.password_hash = password
    user.first_name = first_name
    user.last_name = last_name
    db.commit()

    return UserJSON.from_db(user).json


@secure()
def delete_user(db):
    user = request.environ.get('user_info')
    if user is None:
        raise RuntimeError("delete_user should always have user_info")
    db.delete(user)
    return Message("I have deleted your user.  Why does everyone leave me?").json


def get_user_info(user_id, db):
    user = db.query(User).get(user_id)
    if user is None:
        response.status = 404
        return Error("User %d doesn't exist" % user_id).json

    return UserJSON.from_db(user).json


@secure()
def get_nearby_users(db):
    # Needs user token
    # url params to specify timeframe?
    # SELECT * FROM users WHERE ??????? << TABLE JOINS?
    user = request.environ.get('user_info')
    if user is None:
        raise RuntimeError("get_nearby_users should always have user_info")

    query = text(
    """
        WITH data AS (
            SELECT * FROM observations o
            WHERE age(CURRENT_TIMESTAMP, o.timestamp) < INTERVAL '1 day'
        ), full_set AS (
            -- People Seen by target_user
            SELECT u.* FROM data d
            JOIN devices dev on dev.id = d.device_id
            JOIN users u ON u.id = dev.user_id
            WHERE d.user_id = :target_user

            UNION ALL

            -- People that saw target_user
            SELECT u.* FROM data d
            JOIN users u ON u.id = d.user_id
            JOIN devices dev ON dev.id = d.device_id
            WHERE dev.user_id = :target_user
        )

        -- Combine and order by rate of occurance
        SELECT *, COUNT(id) AS mycount
        FROM full_set
        GROUP BY id, username, first_name, last_name, password_hash
        ORDER BY mycount DESC
    """)
    query = query.bindparams(target_user=user.id)
    seen = db.execute(query).fetchall()
    seen = [UserJSON.from_db(u) for u in seen]
    return Users(seen).json
