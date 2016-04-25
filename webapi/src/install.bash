#! /bin/bash

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

echo "Moving conf files to appropriate locations"
cp "$SCRIPT_DIR/../conf/django.conf" /etc/nginx/sites-enabled
cp "$SCRIPT_DIR/../conf/gunicorn.conf"  /etc/init/

echo "Making sure dependencies are installed"
source "$SCRIPT_DIR/../bin/activate"
pip install -r "$SCRIPT_DIR/../requirements.txt" -q
deactivate

echo "Restarting Services"
service nginx restart
service gunicorn restart
