#!/bin/bash
# Run after the initial deployment and the project directory 
# is created to create a starter .env file.
# Usage: sudo /opt/scripts/init_env.sh <project_name> <deploy_user>

set -e

PROJECT_NAME=$1
DEPLOY_USER=$2

if [ -z "$PROJECT_NAME" ] || [ -z "$DEPLOY_USER" ]; then
  echo "Usage: $0 <project_name> <deploy_user>"
  exit 1
fi

APP_DIR="/var/www/sites/$PROJECT_NAME"
ENV_FILE="$APP_DIR/.env"

if [ -f "$ENV_FILE" ]; then
  echo "⚠️  .env already exists at $ENV_FILE"
  exit 0
fi

echo "📝 Creating starter .env file at $ENV_FILE..."
sudo tee "$ENV_FILE" > /dev/null <<EOF
SECRET_KEY=changeme123
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ALLOWED_HOSTS=127.0.0.1,localhost
EOF

sudo chown "$DEPLOY_USER:www-data" "$ENV_FILE"
sudo chmod 640 "$ENV_FILE"

echo "✅ .env created. Please edit it with real values before running setup_deploy.sh"
