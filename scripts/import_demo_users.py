#!/usr/bin/env python
"""Import demo users from user.sql into SQLite database"""
from app import create_app, db
from app.models.User import User
from datetime import datetime

app = create_app()

# Demo users data from user.sql
demo_users = [
    {
        'id': 11,
        'username': 'NONO',
        'email': 'noelaankunda@gmail.com',
        'password_hash': 'scrypt:32768:8:1$dhRp5WnCchG5n2F6$241a277d394a9953febf8fed2b6d41fa87bc84a0dc36bb3c002e08f5f4db0c0bfaef6489c39da54d5920c37aed3cc758e11baedb7e070164a23b1dce620a6ce9',
        'is_admin': False,
        'last_login': datetime(2025, 7, 23, 21, 30, 45),
        'account_locked': False,
    },
    {
        'id': 12,
        'username': 'SSEKIZIYIVU GRACE',
        'email': 'ssekiziyivugrace55@gmail.com',
        'password_hash': 'scrypt:32768:8:1$2a0Som5MAtsSt77d$b79ba25564501c7febc260fb516b40f92c7e3409a677671a1545382ec910d53b0874d8ff42ed458ae961ce98296e1edf687b9b1f18418cd2ef981a21cb923726',
        'is_admin': True,
        'last_login': datetime(2025, 7, 24, 16, 1, 45),
        'account_locked': False,
    },
    {
        'id': 13,
        'username': 'praise butsilo',
        'email': 'butsilo@gmail.com',
        'password_hash': 'scrypt:32768:8:1$QueekLgaAx8O3yhC$768d486f137573bf50887918be4035405f83e3941c0fe486d4107b719aaaf836ed7678678b992b2affeaf287613e9b7429b8f4138f4c470f1e1537aee86724fd',
        'is_admin': False,
        'account_locked': False,
    },
    {
        'id': 14,
        'username': 'Shakiran Nannyombi',
        'email': 'shakirannannyombi@gmail.com',
        'password_hash': 'scrypt:32768:8:1$nQSacbUpb6J3h1iO$a0903b9a57995ea52670ceac755dd8f1541629c2b69c55b0b61105d5c91efefc0db548f28a38e9591db3767a0c869319fc6f65c15ea27a7131d185de54c7af41',
        'is_admin': False,
        'last_login': datetime(2025, 7, 28, 20, 57, 54),
        'account_locked': False,
    },
    {
        'id': 15,
        'username': 'Shakiran',
        'email': 'devkiran256@gmail.com',
        'password_hash': 'scrypt:32768:8:1$oTURYidcmyGBfpPe$3194675f44be7f43bc555349536f7a80796cde7e874fa27c2042d0c5d84c921a1842b197a1354f65686827a1ba84f5fde807858acd66160109d82cfdc36720d8',
        'is_admin': True,
        'last_login': datetime(2025, 7, 28, 21, 4, 27),
        'account_locked': False,
        'first_name': 'Shakiran',
        'last_name': 'Nannyombi',
        'email_notifications': True,
        'newsletter': False,
        'sms_notifications': False,
        'language': 'en',
        'timezone': 'UTC',
        'two_factor_auth': False,
        'public_profile': True,
        'date_created': datetime(2025, 7, 28, 14, 45, 4),
    },
]

with app.app_context():
    # Check if users already exist
    existing_count = User.query.count()
    if existing_count > 0:
        print(f"Database already has {existing_count} user(s).")
        response = input("Do you want to clear existing users and import demo data? (yes/no): ")
        if response.lower() != 'yes':
            print("Import cancelled.")
            exit(0)
        
        # Clear existing users
        User.query.delete()
        db.session.commit()
        print("Cleared existing users")
    
    # Import demo users
    for user_data in demo_users:
        user = User(**user_data)
        db.session.add(user)
    
    db.session.commit()
    
    print(f"\nSuccessfully imported {len(demo_users)} demo users!")
    print("\nDemo Users:")
    print("-" * 80)
    for user in User.query.all():
        admin_badge = "ADMIN" if user.is_admin else "USER"
        print(f"{admin_badge} | {user.username:25} | {user.email:35}")
    print("-" * 80)
    print(f"\nTotal users in database: {User.query.count()}")
