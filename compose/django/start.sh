#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

python load_seeds.py # load db

python manage.py runserver 0.0.0.0:8000