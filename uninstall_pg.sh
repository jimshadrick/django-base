#!/bin/bash
# uninstall_pg.sh
# Usage: ./uninstall_pg.sh <db_name> <db_user>
# Description: Uninstalls a PostgreSQL database and related user and cleans up connections.

DB_NAME=$1
DB_USER=$2

if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ]; then
  echo "Usage: $0 <db_name> <db_user>"
  exit 1
fi

echo "🧨 Dropping PostgreSQL connections to '$DB_NAME'..."
sudo -u postgres psql -c "REVOKE CONNECT ON DATABASE $DB_NAME FROM public;"
sudo -u postgres psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$DB_NAME';"

echo "🗑️ Dropping database '$DB_NAME'..."
sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DB_NAME;"

echo "👋 Dropping user '$DB_USER' and removing privileges..."
sudo -u postgres psql -c "DROP OWNED BY $DB_USER;"
sudo -u postgres psql -c "DROP ROLE IF EXISTS $DB_USER;"

echo "✅ PostgreSQL cleanup complete for DB: $DB_NAME and USER: $DB_USER."
