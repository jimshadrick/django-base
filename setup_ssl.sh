### `setup_ssl.sh` Script
```bash
#!/bin/bash
# Install and configure SSL for the project using Certbot.
# Pre-requisites: domain must be registered and email must be provided
# Usage: sudo ./setup_ssl.sh <project_name> <your_domain> <your_email>

PROJECT_NAME=$1
DOMAIN=$2
EMAIL=$3

if [ -z "$PROJECT_NAME" ] || [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
  echo "Usage: $0 <project_name> <your_domain> <your_email>"
  exit 1
fi

# 1. Install Certbot
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

# 2. Request Certificate
sudo certbot --nginx --non-interactive --agree-tos -m "$EMAIL" -d "$DOMAIN" -d "www.$DOMAIN" --redirect

# 3. Test Auto-Renewal
sudo certbot renew --dry-run

echo "✅ SSL certificate setup complete for $DOMAIN. HTTPS should now be active."
```

---