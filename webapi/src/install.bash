#! /bin/bash

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
cp "$SCRIPT_DIR/../conf/django.conf" /etc/nginx/sites-enabled
cp "$SCRIPT_DIR/../conf/gunicorn.conf"  /etc/init/
service gunicorn restart
