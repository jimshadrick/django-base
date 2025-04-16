#!/bin/bash
# setup_deploy.sh
# Usage: ./setup_deploy.sh <project_name>
# Description: Creates/updates a Django project deployment on a server

set -e
set -o pipefail

# === PARAMETERS ===
PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
  echo "Usage: $0 <project_name>"
  exit 1
fi

DEPLOY_USER=$(whoami)
APP_DIR="/var/www/sites/$PROJECT_NAME"
TEMP_ENV_BACKUP="/tmp/project_env_backup_$PROJECT_NAME"
REPO_URL="https://github.com/your-user/$PROJECT_NAME.git"  # <-- Replace manually for each project

echo "📁 Ensuring project directory exists and is owned by $DEPLOY_USER..."
sudo mkdir -p "$APP_DIR"
sudo chown -R "$DEPLOY_USER:www-data" "$APP_DIR"
sudo chmod -R 755 "$APP_DIR"

cd "$APP_DIR"

# === Generate .env scaffold if missing ===
ENV_FILE="$APP_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "📝 Creating starter .env file..."
  cat <<EOF > "$ENV_FILE"
SECRET_KEY=changeme123
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ALLOWED_HOSTS=127.0.0.1,localhost
EOF
  sudo chown "$DEPLOY_USER:www-data" "$ENV_FILE"
  sudo chmod 640 "$ENV_FILE"
fi

# === Backup .env file before wiping directory ===
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
source .venv/bin/activate

# === Post-deploy script ===
echo "🚀 Running post-deployment script..."
./dj-post-deploy.sh