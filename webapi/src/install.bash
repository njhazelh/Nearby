#! /bin/bash

BASEDIR = $(dirname "$0")

cp $BASEDIR/../conf/django.conf /etc/nginx/sites-enabled
cp $BASEDIR/../conf/gunicorn.conf /etc/init/
service gunicorn restart
