#! /bin/bash

echo "${BASH_SOURCE[0]}"
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
echo $SCRIPT_DIR

cp "$SCRIPT_DIR/../conf/django.conf" /etc/nginx/sites-enabled
cp "$SCRIPT_DIR/../conf/gunicorn.conf"  /etc/init/
service gunicorn restart
