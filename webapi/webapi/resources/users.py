"""
This file contains resource functions that access and manipulate user data
"""

def get_personal_info():
    # Needs user token
    # SELECT * FROM users WHERE id = token.userid
    return "Here is your personal info"

def create_new_user():
    # Not authed
    # Rate-limited?
    # INSERT INTO users VALUE (user_info)
    return "I have created a new user for you"

def change_personal_info():
    # Needs user token
    # Needs body info
    # UPDATE users SET user_info=new_info WHERE user_id = token.userid
    return "I have changed your personal info"

def delete_user():
    # Needs user token
    # DELETE FROM users WHERE user.id = token.userid
    return "I have deleted your user.  Why does everyone leave me?"

def get_user_info(user_id):
    # Not authed?
    # SELECT * FROM users WHERE user.id = user_id
    return "This is everything I know about, %s: jack-shit" % user_id

def get_nearby_users():
    # Needs user token
    # url params to specify timeframe?
    # SELECT * FROM users WHERE ??????? << TABLE JOINS?
    return "People might be nearby.  Who knows? Not I."
