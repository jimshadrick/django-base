#!/bin/bash
# setup_deploy.sh
# Usage: ./setup_deploy.sh <project_name> <deploy_user> [--skip-post]
# Description: Creates a new project directory and performs a Django project deployment on the server
# Change Log:
# 2025-04-28: Add commands to restart Gunicorn workers and restart Nginx after deployment.
# 2025-07-28: Modified backup and restore of .env to use .env.prod 
# 2025-08-06: Parameterized project name and updated call to post_deploy script accordingly.

set -e
set -o pipefail

PROJECT_NAME=$1
DEPLOY_USER=$2
SKIP_POST=$3

if [ -z "$PROJECT_NAME" ] || [ -z "$DEPLOY_USER" ]; then
  echo "Usage: $0 <project_name> <deploy_user> [--skip-post]"
  exit 1
fi

APP_DIR="/var/www/sites/$PROJECT_NAME"
TEMP_ENV_BACKUP="/tmp/project_env_backup_$PROJECT_NAME"
REPO_URL="https://github.com/jimshadrick/django-base.git"

echo "📁 Ensuring project directory exists and is owned by $DEPLOY_USER & www-data group ..."
sudo mkdir -p "$APP_DIR"
sudo chown -R "$DEPLOY_USER:www-data" "$APP_DIR"
sudo chmod -R 755 "$APP_DIR"

cd "$APP_DIR"

# === Backup .env.prod file before wiping directory ===
ENV_FILE="$APP_DIR/.env.prod"
if [ -f .env.prod ]; then
  echo "🔐 Backing up .env.prod file temporarily..."
  cp .env.prod "$TEMP_ENV_BACKUP"
fi

# === Remove old virtual environment and contents ===
echo "🧹 Removing existing virtual environment (if any)..."
rm -rf .venv

echo "🧼 Cleaning project directory (excluding .env backup)..."
find . -mindepth 1 ! -name "$(basename "$TEMP_ENV_BACKUP")" -exec rm -rf {} +

# === Clone repo ===
echo "📦 Cloning repository..."
git clone "$REPO_URL" .

# === Restore .env.prod ===
if [ -f "$TEMP_ENV_BACKUP" ]; then
  echo "🔄 Restoring .env.prod file..."
  mv "$TEMP_ENV_BACKUP" .env.prod
  # Create symlink so Gunicorn can find the environment file
  ln -sf .env.prod .env
else
  echo "⚠️ No .env.prod backup found - you may need to create environment files"
fi


# === Sync and activate environment ===
echo "📦 Installing dependencies with uv..."
/home/$DEPLOY_USER/.local/bin/uv sync

echo "⚙️  Activating virtual environment..."
cd "$APP_DIR"
source .venv/bin/activate

# === Post deployment script ===
if [ "$SKIP_POST" != "--skip-post" ]; then
  echo "🚀 Running post-deployment script..."
  ./post_deploy.sh "$PROJECT_NAME"
else
  echo "⚠️ Skipping post-deployment script."
fi

# === Restart services to load new code ===
sudo systemctl restart gunicorn-$PROJECT_NAME.service
sudo systemctl restart gunicorn-$PROJECT_NAME.socket
sudo systemctl restart nginx