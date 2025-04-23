#!/bin/bash
# post_deploy.sh
# Usage: ./.venv/bin/activate && ./post_deploy.sh
# Description: Post-deployment script for Django

set -e # Exit immediately if a command exits with a non-zero status.

echo "--- Running Database Migrations ---"
uv run python manage.py migrate --noinput

echo "--- Collecting Static Files ---"
# Ensure the staticfiles directory exists if collectstatic expects it
mkdir -p staticfiles
uv run python manage.py collectstatic --noinput --ignore="vendor/*"

echo "--- Initializing Site (Custom Command) ---"
uv run python manage.py init_site # Ensure this command is idempotent or safe to run repeatedly

echo "Reloading systemd"
sudo systemctl daemon-reload

echo "Restarting Gunicorn socket and service..."
sudo systemctl restart gunicorn-djbaseapp.socket
sudo systemctl restart gunicorn-djbaseapp.service

echo "Reloading Nginx"
sudo nginx -t && sudo systemctl reload nginx

echo "--- Deployment Script Finished ---"