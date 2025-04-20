#!/bin/bash
# setup_configs.sh
# Usage: sudo ./setup_configs.sh <project_name> <deploy_user>
# Change Log:
# 2025-04-18: Add [Socket] ownership parameters SocketUser & SocketGroup.
# 2025-04-18: Modify Nginx config to include default_server and handle server name properly.
# 2025-04-18: Add a step to disable the default site.
# 2025-04-18: Add a more thorough service reload and restart sequence.
# 2025-04-20: Removed the UV_PATH from the ExecStart line to run the gunicorn binary directly.
# 2025-04-20: Bind to my actual Unix socket file $SOCKET_PATH and not use fd://3
# 2025-04-20: Corrected the import path to project.wsgi:application (not $PROJECT_NAME.wsgi:application)


PROJECT_NAME=$1
DEPLOY_USER=$2

if [ -z "$PROJECT_NAME" ] || [ -z "$DEPLOY_USER" ]; then
  echo "Usage: $0 <project_name> <deploy_user>"
  exit 1
fi

APP_DIR="/var/www/sites/$PROJECT_NAME"
SOCKET_PATH="/run/$PROJECT_NAME.sock"
#UV_PATH="/home/$DEPLOY_USER/.local/bin/uv"
GUNICORN_PATH="$APP_DIR/.venv/bin/gunicorn"

echo "🛠️ Generating and deploying Gunicorn and Nginx configs for '$PROJECT_NAME'..."

# === Ensure DEPLOY_USER has access to project files ===
sudo chown -R $DEPLOY_USER:www-data "$APP_DIR"
sudo chmod 640 "$APP_DIR/.env"
sudo chmod 755 "$APP_DIR"

# === Gunicorn socket ===
cat <<EOF | sudo tee /etc/systemd/system/gunicorn-$PROJECT_NAME.socket > /dev/null
[Unit]
Description=gunicorn socket for $PROJECT_NAME

[Socket]
ListenStream=$SOCKET_PATH
SocketUser=$DEPLOY_USER
SocketGroup=www-data
SocketMode=0660

[Install]
WantedBy=sockets.target
EOF

# === Gunicorn service ===
cat <<EOF | sudo tee /etc/systemd/system/gunicorn-$PROJECT_NAME.service > /dev/null
[Unit]
Description=gunicorn daemon for $PROJECT_NAME
Requires=gunicorn-$PROJECT_NAME.socket
After=network.target

[Service]
User=$DEPLOY_USER
Group=www-data
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$GUNICORN_PATH \\
          --access-logfile - \\
          --workers 3 \\
          --bind unix:$SOCKET_PATH \\
          project.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# === Nginx config ===
NGINX_AVAILABLE="/etc/nginx/sites-available/$PROJECT_NAME"
NGINX_ENABLED="/etc/nginx/sites-enabled/$PROJECT_NAME"

cat <<EOF | sudo tee "$NGINX_AVAILABLE" > /dev/null
server {
    listen 80 default_server;
    server_name YOUR_DROPLET_IP;  # Will be replaced with your_domain.com later

    access_log /var/log/nginx/$PROJECT_NAME.access.log;
    error_log /var/log/nginx/$PROJECT_NAME.error.log;

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    location /static/ {
        root $APP_DIR;
        access_log off;
        expires 30d;
    }

    location / {
        proxy_set_header Host \$http_host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_pass http://unix:$SOCKET_PATH;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
EOF

# === Back up default site if it exists ===
if [ -f "/etc/nginx/sites-enabled/default" ]; then
  sudo cp /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default.bak
  echo "📁 Backed up default Nginx site configuration to /etc/nginx/sites-available/default.bak"
fi

# === Disable the default site ===
sudo rm -f /etc/nginx/sites-enabled/default
echo "🔄 Disabled default Nginx site"

# === Enable Nginx site ===
sudo ln -sf "$NGINX_AVAILABLE" "$NGINX_ENABLED"

# === Reload systemd and services ===
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl stop gunicorn-$PROJECT_NAME.socket
sudo systemctl stop gunicorn-$PROJECT_NAME.service
sudo rm -f $SOCKET_PATH  # Clean up any existing socket
sudo systemctl enable gunicorn-$PROJECT_NAME.socket
sudo systemctl start gunicorn-$PROJECT_NAME.socket

# === Test the socket activation ===
echo "Testing socket activation..."
curl --unix-socket $SOCKET_PATH http://localhost/ || echo "Socket test failed, but continuing deployment..."

# === Test and reload Nginx ===
sudo nginx -t && sudo systemctl restart nginx

# === Configure logrotate for Nginx project logs ===
LOGROTATE_CONFIG_PATH="/etc/logrotate.d/$PROJECT_NAME"

sudo tee "$LOGROTATE_CONFIG_PATH" > /dev/null <<EOF
/var/log/nginx/$PROJECT_NAME*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 640 www-data adm
    sharedscripts
    postrotate
        [ -s /run/nginx.pid ] && kill -USR1 \$(cat /run/nginx.pid)
    endscript
}
EOF

echo "🧾 Logrotate configuration added at $LOGROTATE_CONFIG_PATH"

echo "✅ Deployment for '$PROJECT_NAME' completed."
echo ""
echo "📋 Next steps:"
echo "  1. Replace 'YOUR_DROPLET_IP' in $NGINX_AVAILABLE with your actual IP: $HOSTNAME_IP"
echo "  2. When you get a domain, update the server_name directive"
echo "  3. For SSL setup, run: sudo certbot --nginx -d yourdomain.com"