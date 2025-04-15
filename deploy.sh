#!/bin/bash
# Post-deployment script for Django

set -e # Exit immediately if a command exits with a non-zero status.

echo "--- Running Database Migrations ---"
uv run python manage.py migrate --noinput

echo "--- Collecting Static Files ---"
# Ensure the staticfiles directory exists if collectstatic expects it
mkdir -p staticfiles
uv run python manage.py collectstatic --noinput

echo "--- Initializing Site (Custom Command) ---"
uv run python manage.py init_site # Ensure this command is idempotent or safe to run repeatedly

echo "--- Deployment Script Finished ---"