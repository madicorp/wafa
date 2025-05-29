#!/bin/bash
set -e

python manage.py compilemessages
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:80
