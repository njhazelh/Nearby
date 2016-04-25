#! /usr/bin/env python

from bottle import run, post, get, put, delete

@get('/api')
def index():
    return "Hello, world!"

@get('/api/access')
def login():
    return "login token value thing"

@delete('/api/access')
def logout():
    return "You are now logged out!"

@get('/api/users')
def get_personal_info():
    return "Here is your personal info"

@post('/api/users')
def create_new_user():
    return "I have created a new user for you"

@put('/api/users')
def change_personal_info():
    return "I have changed your personal info"

@delete('/api/users')
def delete_user():
    return "I have deleted your user.  Why does everyone leave me?"

@get('/api/users/<user_id:int>')
def get_user_info(user_id):
    return "This is everything I know about, %s: jack-shit" % user_id

@get('/api/users/nearby')
def get_nearby_users():
    return "People might be nearby.  Who knows? Not I."

@post('/api/observations')
def record_observation():
    return "I'll remember that for the future."

@post('/api/devices')
def add_new_device():
    return "Device associated with your account. Forgot the others"

if __name__ == "__main__":
    run(server="gunicorn", host='localhost', port=9000)
