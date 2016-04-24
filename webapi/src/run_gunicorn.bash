#! /bin/bash


source bin/activate


# gunicorn --name webapi --pythonpath=webapi --bind 127.0.0.1:9000 webapi.wsgi:application
exec gunicorn \
    --name=webapi \
    --pythonpath=webapi \
    --bind=127.0.0.1:9000 \
    --config /etc/gunicorn.d/gunicorn.py \
    webapi.wsgi:application
