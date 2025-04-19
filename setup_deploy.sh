# setup_deploy.sh
#!/bin/bash
# Usage: ./setup_deploy.sh <project_name> <deploy_user> [--skip-post]
# Description: Creates a new project directory and performs a Django project deployment on the server

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

# === Backup .env file before wiping directory ===
ENV_FILE="$APP_DIR/.env"
if [ -f .env ]; then
  echo "🔐 Backing up .env file temporarily..."
  cp .env "$TEMP_ENV_BACKUP"
fi

# === Remove old virtual environment and contents ===
echo "🧹 Removing existing virtual environment (if any)..."
rm -rf .venv

echo "🧼 Cleaning project directory (excluding .env backup)..."
find . -mindepth 1 ! -name "$(basename "$TEMP_ENV_BACKUP")" -exec rm -rf {} +

# === Clone repo ===
echo "📦 Cloning repository..."
git clone "$REPO_URL" .

# === Restore .env ===
if [ -f "$TEMP_ENV_BACKUP" ]; then
  echo "🔄 Restoring .env file..."
  mv "$TEMP_ENV_BACKUP" .env
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
  ./post_deploy.sh
else
  echo "⚠️ Skipping post-deployment script."
fi
