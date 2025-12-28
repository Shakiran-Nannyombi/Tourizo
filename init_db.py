#!/usr/bin/env python
"""Initialize the SQLite database"""
from app import create_app, db

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database created successfully!")
    print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
