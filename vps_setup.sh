#!/bin/bash
set -e
set -o pipefail

REPO_URL="https://github.com/jimshadrick/django-base.git"
PROJECT_DIR="/var/www/sites/djbaseapp"

echo "==> Navigating to project directory..."
cd "$PROJECT_DIR"

echo "==> Removing existing virtual environment (if any)..."
rm -rf .venv

echo "==> Cleaning project directory..."
# Preserve vps_setup.sh and .env during cleanup
find . -mindepth 1 \
  ! -name 'vps_setup.sh' \
  ! -name '.env' \
  -exec rm -rf {} +

echo "==> Cloning repo into current directory..."
git clone "$REPO_URL" . 

echo "==> Reinstalling dependencies with uv..."
uv sync

echo "==> Activating virtual environment..."
source .venv/bin/activate

echo "==> Running post-deployment script..."
./deploy.sh
