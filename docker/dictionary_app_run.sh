#!/bin/bash

python /dictionary/docker/wait_for_postgres.py

pwd

ls

python manage.py migrate

python manage.py runserver 0.0.0.0:8000
