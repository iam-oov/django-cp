#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

wait-for-it my-mysql:3007

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

python manage.py createsuperuserwithpassword \
	--username root \
	--password 1234abcd \
	--email admin@mail.org \
	--preserve

python manage.py runserver 0.0.0.0:8000
