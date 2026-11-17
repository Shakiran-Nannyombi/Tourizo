#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Building project..."

# Install dependencies
pip install -r requirements.txt

# Verify build (ensure all dependencies and entry points are valid)
echo "Running build tests..."
python -m pytest tests/test_build.py

# Create instance folder if it doesn't exist
mkdir -p instance

# Create missing tables and demo data. The committed SQLite file is already
# stamped at the Alembic head, and those migrations only alter existing
# tables, so `flask db upgrade` leaves the database empty.
echo "Preparing database..."
python -c "from app import create_app; create_app()"

echo "Build complete!"
