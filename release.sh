#!/bin/bash

set -e
uv run manage.py migrate
uv run manage.py collectstatic --noinput
uv run manage.py createsuperuser
