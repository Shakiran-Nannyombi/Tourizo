#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Building project..."

# Install dependencies
pip install -r requirements.txt

# Verify build (ensure all dependencies are importable)
echo "Verifying build..."
python scripts/verify_build.py

# Create instance folder if it doesn't exist
mkdir -p instance

# Flask DB migrations
export FLASK_APP=run.py
flask db upgrade

# Seed database with demo data (essential for SQLite persistence on Render)
echo "Seeding database..."
python create_admin.py
python scripts/seed_tours.py
python scripts/add_demo_bookings.py
python scripts/add_demo_reviews.py
python scripts/add_image_galleries.py

echo "Build complete!"
