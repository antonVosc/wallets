#!/bin/sh
set -e

echo "Creating test database if not exists..."
psql -h db -U wallet -d wallet_db -tc \
  "SELECT 1 FROM pg_database WHERE datname='wallet_test'" \
  | grep -q 1 \
  || psql -h db -U wallet -d wallet_db \
     -c "CREATE DATABASE wallet_test;"

echo "Running migrations..."
alembic upgrade head

echo "Done."