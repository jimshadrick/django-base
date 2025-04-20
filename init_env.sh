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
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=supersecretkey
DATABASE_URL=postgres://postgres:postgres@db:5432/mydbname
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
CONN_MAX_AGE=60
MAILGUN_API_KEY=changeme
MAILGUN_DOMAIN=sandboxid.mailgun.org
DEFAULT_FROM_EMAIL=admin@localhost
SITE_DOMAIN=mydomain.com
SITE_NAME=mydomain
EOF

sudo chown "$DEPLOY_USER:www-data" "$ENV_FILE"
sudo chmod 640 "$ENV_FILE"

echo "✅ .env created. Please edit it with real values before running setup_deploy.sh"
