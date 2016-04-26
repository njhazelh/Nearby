#! /usr/bin/env python

from bottle import request, response, app, run, hook
from resources import access, devices, observations, users


@hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


def setup_routing(app):
    app.route('/api/access', 'POST', access.login)
    app.route('/api/access', 'DELETE', access.logout)
    app.route('/api/users', 'GET', users.get_personal_info)
    app.route('/api/users', 'POST', users.create_new_user)
    app.route('/api/users', 'PUT', users.change_personal_info)
    app.route('/api/users', 'DELETE', users.delete_user)
    app.route('/api/users/<user_id:int>', 'GET', users.get_user_info)
    app.route('/api/users/nearby', 'GET', users.get_nearby_users)
    app.route('/api/devices', 'GET', devices.get_devices)
    app.route('/api/devices', 'POST', devices.add_new_device)
    app.route('/api/observations', 'POST', observations.record_observation)


def setup_middleware(app):
    return app

if __name__ == "__main__":
    app = app()
    setup_routing(app)
    app = setup_middleware(app)
    # add server='gunicorn' for deployment and remove reloader
    run(host='localhost', port=9000, app=app, reloader=True)
