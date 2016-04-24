#! /bin/bash

cp ../conf/django.conf /etc/nginx/sites-enabled
cp ../conf/gunicorn.conf /etc/init/
service gunicorn restart
