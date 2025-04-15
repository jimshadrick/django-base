#!/bin/bash
# Cleanup script prepares the server for a new deployment

set -e
set -o pipefail

REPO_URL="https://github.com/jimshadrick/django-base.git"
PROJECT_DIR="/var/www/sites/djbaseapp"
TEMP_ENV_BACKUP="/tmp/project_env_backup"

echo "==> Navigating to project directory..."
cd "$PROJECT_DIR"

# Preserve .env file temporarily
if [ -f .env ]; then
  echo "==> Backing up .env file temporarily..."
  cp .env "$TEMP_ENV_BACKUP"
fi

echo "==> Removing existing virtual environment (if any)..."
rm -rf .venv

echo "==> Cleaning project directory (fully)..."
# Now we can safely delete everything
find . -mindepth 1 -exec rm -rf {} +

echo "==> Cloning repo into current directory..."
git clone "$REPO_URL" .

# Restore .env if it was backed up
if [ -f "$TEMP_ENV_BACKUP" ]; then
  echo "==> Restoring .env file..."
  mv "$TEMP_ENV_BACKUP" .env
fi

echo "==> Installing dependencies with uv..."
uv sync

echo "==> Activating virtual environment..."
source .venv/bin/activate

echo "==> Running post-deployment script..."
./deploy.sh





