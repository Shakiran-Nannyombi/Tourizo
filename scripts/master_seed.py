#!/usr/bin/env python3
import sys
import os
import uuid
import random
from datetime import datetime, timedelta, date, time
from decimal import Decimal

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.User import User
from app.models.Tour import Tour, TourItineraryDay
from app.models.Category import Category
from app.models.Booking import Booking
from app.models.Review import Review

def generate_reference():
    return f"BK{uuid.uuid4().hex[:8].upper()}"

def seed_users():
    print("Seeding users...")
    demo_users = [
        {'username': 'NONO', 'email': 'noelaankunda@gmail.com', 'is_admin': False, 'password_hash': 'scrypt:32768:8:1$dhRp5WnCchG5n2F6$241a277d394a9953febf8fed2b6d41fa87bc84a0dc36bb3c002e08f5f4db0c0bfaef6489c39da54d5920c37aed3cc758e11baedb7e070164a23b1dce620a6ce9'},
        {'username': 'Grace', 'email': 'ssekiziyivugrace55@gmail.com', 'is_admin': True, 'password_hash': 'scrypt:32768:8:1$2a0Som5MAtsSt77d$b79ba25564501c7febc260fb516b40f92c7e3409a677671a1545382ec910d53b0874d8ff42ed458ae961ce98296e1edf687b9b1f18418cd2ef981a21cb923726'},
        {'username': 'Praise', 'email': 'butsilo@gmail.com', 'is_admin': False, 'password_hash': 'scrypt:32768:8:1$QueekLgaAx8O3yhC$768d486f137573bf50887918be4035405f83e3941c0fe486d4107b719aaaf836ed7678678b992b2affeaf287613e9b7429b8f4138f4c470f1e1537aee86724fd'},
        {'username': 'Shakiran', 'email': 'shakirannannyombi@gmail.com', 'is_admin': False, 'password_hash': 'scrypt:32768:8:1$nQSacbUpb6J3h1iO$a0903b9a57995ea52670ceac755dd8f1541629c2b69c55b0b61105d5c91efefc0db548f28a38e9591db3767a0c869319fc6f65c15ea27a7131d185de54c7af41'},
        {'username': 'DevKiran', 'email': 'devkiran256@gmail.com', 'is_admin': True, 'first_name': 'Shakiran', 'last_name': 'Nannyombi', 'password_hash': 'scrypt:32768:8:1$oTURYidcmyGBfpPe$3194675f44be7f43bc555349536f7a80796cde7e874fa27c2042d0c5d84c921a1842b197a1354f65686827a1ba84f5fde807858acd66160109d82cfdc36720d8'}
    ]
    for u_data in demo_users:
        if not User.query.filter_by(email=u_data['email']).first():
            user = User(**u_data)
            db.session.add(user)
    db.session.commit()
    print("Users seeded.")

def seed_bookings():
    print("Seeding bookings...")
    users = User.query.all()
    tours = Tour.query.filter_by(is_active=True).all()
    if not users or not tours:
        print("Missing users or tours for bookings.")
        return
    
    for user in users:
        for i in range(2):
            tour = random.choice(tours)
            booking = Booking(
                reference=generate_reference(),
                user_id=user.id,
                tour_id=tour.id,
                full_name=f"{user.username}",
                email=user.email,
                phone="+256700000000",
                booking_date=date.today() + timedelta(days=random.randint(5, 30)),
                booking_time=time(9, 0),
                num_people=random.randint(1, 4),
                total_amount=Decimal(tour.price * 1000), # Simple multiplier for demo
                payment_method='momo',
                payment_status='paid',
                payment_reference=f"REF{random.randint(1000, 9999)}",
                order_tracking_id=f"TRK{uuid.uuid4().hex[:8].upper()}"
            )
            db.session.add(booking)
    db.session.commit()
    print("Bookings seeded.")

def seed_reviews():
    print("Seeding reviews...")
    users = User.query.all()
    tours = Tour.query.all()
    templates = [
        "Absolutely amazing experience!",
        "Great tour overall!",
        "Decent experience.",
        "Beautiful scenery and great guide."
    ]
    for tour in tours:
        selected_users = random.sample(users, min(2, len(users)))
        for user in selected_users:
            review = Review(
                rating=random.randint(4, 5),
                comment=random.choice(templates),
                reviewer_name=user.username,
                reviewer_email=user.email,
                is_verified=True,
                is_approved=True,
                tour_id=tour.id,
                user_id=user.id
            )
            db.session.add(review)
    db.session.commit()
    print("Reviews seeded.")

def main():
    app = create_app()
    with app.app_context():
        seed_users()
        seed_bookings()
        seed_reviews()
        print("Master seeding completed.")

if __name__ == "__main__":
    main()
