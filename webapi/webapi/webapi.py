#! /usr/bin/env python

from bottle import request, response, app, run, hook
from resources import access, devices, observations, users

from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from data.db_models import Base
from sqlalchemy.orm import sessionmaker


@hook('before_request')
def strip_path():
    """
    pre routing hook to make "/x/y/z/" the same as "/x/y/z"
    """
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


def setup_routing(app):
    """
    Configure url routing for application

    :param app: The bottle application object
    """
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


if __name__ == "__main__":
    app = app()
    engine = create_engine(
        "postgresql://django:svqVUoATZq@localhost:5432/nearby")
    create_session = sessionmaker(bind=engine)
    plugin = sqlalchemy.Plugin(engine, Base.metadata,
                               keyword='db', create=True,
                               commit=True, use_kwargs=True)
    app.install(plugin)
    setup_routing(app)
    # add server='gunicorn' for deployment and remove reloader
    run(host='localhost', port=9000, app=app, reloader=True, debug=True)
