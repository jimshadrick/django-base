#!/bin/bash
# uninstall_cert.sh
# Usage: ./uninstall_cert.sh
# Description: Uninstalls Cloudflare origin certificate files

echo "🔍 Checking for Cloudflare origin certificate files..."

CERTS=(
  "/etc/ssl/certs/cloudflare_origin.pem"
  "/etc/ssl/private/cloudflare_origin.key"
)

for FILE in "${CERTS[@]}"; do
  if [[ -f "$FILE" ]]; then
    echo "✅ Found: $FILE"
  else
    echo "❌ Not found: $FILE"
  fi
done

read -p "❓ Do you want to delete these files? (y/n): " CONFIRM

if [[ "$CONFIRM" == "y" ]]; then
  for FILE in "${CERTS[@]}"; do
    if [[ -f "$FILE" ]]; then
      sudo rm -f "$FILE"
      echo "🗑️ Deleted: $FILE"
    fi
  done
else
  echo "👍 Leaving certs intact."
fi
