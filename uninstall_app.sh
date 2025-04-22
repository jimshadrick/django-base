#!/bin/bash
# uninstall_app.sh
# Usage: sudo ./uninstall_app.sh <project_name>
# Descripion: Uninstalls a Django project from the server
set -e

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
  echo "Usage: $0 <project_name>"
  exit 1
fi

echo "🛑 Stopping and disabling Gunicorn services for $PROJECT_NAME..."
sudo systemctl stop gunicorn-$PROJECT_NAME.service || true
sudo systemctl stop gunicorn-$PROJECT_NAME.socket || true
sudo systemctl disable gunicorn-$PROJECT_NAME.service || true
sudo systemctl disable gunicorn-$PROJECT_NAME.socket || true

echo "🧹 Removing Gunicorn systemd unit files..."
sudo rm -f /etc/systemd/system/gunicorn-$PROJECT_NAME.service
sudo rm -f /etc/systemd/system/gunicorn-$PROJECT_NAME.socket

echo "🧼 Cleaning up leftover socket file..."
sudo rm -f /run/$PROJECT_NAME.sock

echo "🧾 Reloading systemd daemon..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl reset-failed

echo "🧯 Removing Nginx site config for $PROJECT_NAME..."
sudo rm -f /etc/nginx/sites-enabled/$PROJECT_NAME
sudo rm -f /etc/nginx/sites-available/$PROJECT_NAME
sudo rm -f /etc/logrotate.d/$PROJECT_NAME

echo "🗑️ Removing Nginx logs for $PROJECT_NAME..."
sudo rm -f /var/log/nginx/${PROJECT_NAME}.access.log*
sudo rm -f /var/log/nginx/${PROJECT_NAME}.error.log*

echo "🔄 Restarting Nginx to apply changes..."
sudo nginx -t && sudo systemctl restart nginx

echo "📁 Deleting application directory..."
sudo rm -rf /var/www/sites/$PROJECT_NAME

echo "✅ $PROJECT_NAME has been completely removed from the server."
