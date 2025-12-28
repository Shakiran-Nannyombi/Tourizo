#!/usr/bin/env python
"""Create or update admin user with known password"""
from app import create_app, db
from app.models.User import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Check if admin user exists
    admin = User.query.filter_by(email='devkiran256@gmail.com').first()
    
    if admin:
        print(f"Found existing admin user: {admin.username}")
        # Update password
        new_password = 'admin123'
        admin.password_hash = generate_password_hash(new_password)
        admin.is_admin = True
        db.session.commit()
        print(f"\n✓ Password updated for admin user!")
    else:
        # Create new admin user
        print("Creating new admin user...")
        new_password = 'admin123'
        admin = User(
            username='admin',
            email='admin@tourizo.com',
            password_hash=generate_password_hash(new_password),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f"\n✓ New admin user created!")
    
    print("\n" + "=" * 80)
    print("ADMIN LOGIN CREDENTIALS")
    print("=" * 80)
    print(f"Email:    {admin.email}")
    print(f"Password: {new_password}")
    print("=" * 80)
    print(f"\nLogin URL: http://localhost:5000/login")
    print("\nIMPORTANT: Change this password after first login!")
    print("=" * 80)
