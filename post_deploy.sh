#!/bin/bash
# post_deploy.sh
# Usage: ./.venv/bin/activate && ./post_deploy.sh <project_name>
# Description: Post-deployment script for Django
# Change log:
# 2025-08-06: Parameterized project name and updated gunicorn services accordingly.

set -e # Exit immediately if a command exits with a non-zero status.

PROJECT_NAME=$1

# Ensure project name is provided
if [ -z "$PROJECT_NAME" ]; then
  echo "Usage: $0 <project_name>"
  exit 1
fi

# Set Django environment for production
export DJANGO_ENV=prod

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
sudo systemctl restart gunicorn-$PROJECT_NAME.socket
sudo systemctl restart gunicorn-$PROJECT_NAME.service


echo "Reloading Nginx"
sudo nginx -t && sudo systemctl reload nginx

echo "--- Deployment Script Finished ---"