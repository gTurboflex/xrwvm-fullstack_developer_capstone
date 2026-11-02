#!/bin/sh
set -eu
python manage.py migrate --noinput
python manage.py load_cars
python manage.py collectstatic --noinput
exec "$@"
