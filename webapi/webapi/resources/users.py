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


class UsersJSON(JSONResponse):

    """
    An Object for generating JSON for a list of Users.
    """

    def __init__(self, users):
        self.users = users

    @staticmethod
    def from_db(db_users):
        """
        Convert a list of database user info to a list of JSON user info
        """
        return UsersJSON([UserJSON.from_db(u) for u in db_users])


class UserJSON(JSONResponse):

    """
    An Object for generating JSON for a single User.
    {
        "id": <integer>,
        "username": <string>,
        "first_name": <string>,
        "last_name": <password>,
    }
    """

    def __init__(self, user_id, username, first_name, last_name):
        self.id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def from_db(db_user):
        """
        Convert a database user to JSON
        """
        return UserJSON(db_user.id, db_user.username,
                        db_user.first_name, db_user.last_name)


@secure()
def get_personal_info(db):
    """
    Get the personal information for the logged in user.

    :param db: The database session
    :returns: Information of logged in user in a dictionary format.
    """
    return UserJSON.from_db(request.environ['user_info']).json


def create_new_user(db):
    """
    Create a new User.  JSON must include all fields.

    JSON body with all fields is:

    {
        "username": <string>,
        "password": <string>,
        "first_name": <string>,
        "last_name": <string>,
    }

    :param db: The database session
    :returns: JSON containing the created user info if successful
        Otherwise, returns error information in JSON format.
    """
    try:
        # Access and validate new user info from JSON body
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
        response.status = 400  # Bad Request
        return Error("Missing JSON with valid username, password, " +
                     "first_name, last_name").json

    # Check that the username doesn't already exist
    count = db.query(User).filter(User.username == username).count()
    if count != 0:
        response.status = 400
        return Error("'%s' already exists" % username).json

    # Insert User into database
    user = User(username=username,
                password_hash=password,
                first_name=first_name,
                last_name=last_name)
    db.add(user)
    db.commit()

    return UserJSON.from_db(user).json


@secure()
def change_personal_info(db):
    """
    A resource for changing user info.  Update request can contain 0 or more
    fields to change the user.  Missing fields will not be updated.

    JSON body with all fields is:

    {
        "username": <string>,
        "password": <string>,
        "first_name": <string>,
        "last_name": <string>,
    }

    :param db: The database session
    :returns: Error JSON on failure or updated user JSON on success.
    """

    # Get User info from request environment.
    user = request.environ.get('user_info')
    if user is None:
        raise RuntimeError('change_personal_info should always have user_info')

    # Get Update JSON from body. Return unchanged user if no body.
    data = request.json
    if data is None:
        return UserJSON.from_db(user).json

    # Validate JSON body
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

    # Check username for originality if changing
    username = data.get('username', user.username)
    if username != user.username:
        count = db.query(User).filter(User.username == username).count()
        if count != 0:
            response.status = 400
            return Error("'%s' already exists" % username).json

    # Update fields and send to database
    user.username = username
    user.password_hash = data.get('password', user.password_hash)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    db.commit()

    return UserJSON.from_db(user).json


@secure()
def delete_user(db):
    """
    Delete the account of the currently logged in user.

    :param db: The database session
    :returns: MessageJSON indicating success.
    """
    user = request.environ.get('user_info')
    if user is None:
        raise RuntimeError("delete_user should always have user_info")
    db.delete(user)
    return Message("User account deleted.  Why does everyone leave me?").json


def get_user_info(user_id, db):
    """
    Get the information of a specific user identified by `user_id`.

    :param user_id: The user_id of the user to get info for.
    :param db: The database session.
    :returns: Error JSON on user not found, else User JSON on success.
    """
    user = db.query(User).get(user_id)
    if user is None:
        response.status = 404
        return Error("User %d doesn't exist" % user_id).json

    return UserJSON.from_db(user).json


@secure()
def get_nearby_users(db):
    """
    Get the users that have seen the current user or been seen by the current
    user within a recent period (1 day).

    :param db: The database session
    :returns: A list of recently nearby users. Ordered by number of observations
        regarding them.
    """
    # Get User info from request environment.  Needed for user.id
    user = request.environ.get('user_info')
    if user is None:
        raise RuntimeError("get_nearby_users should always have user_info")

    query = text(
        """
        WITH data AS (
            SELECT * FROM observations o
            WHERE age(CURRENT_TIMESTAMP, o.timestamp) < INTERVAL '1 minute'
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
    return UsersJSON.from_db(seen).json
