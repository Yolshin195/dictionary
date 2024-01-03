#!/bin/bash

python /dictionary/docker/wait_for_postgres.py

python manage.py migrate

python manage.py loaddata sentences/language.yaml

python manage.py runserver 0.0.0.0:8000
