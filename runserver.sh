#!/bin/bash

poetry run python manage.py migrate
poetry run python manage.py collectstatic --no-input
poetry run gunicorn \
            --bind=0.0.0.0:80 \
            --access-logfile=- \
            --threads=4 \
            enough_recipes.wsgi
