#!/usr/bin/env python3
"""
Script to add demo bookings for users in the database.
This creates sample bookings with different payment statuses and realistic data.
"""

import sys
import os
import uuid
from datetime import datetime, timedelta, date, time
from decimal import Decimal

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.Booking import Booking
from app.models.Tour import Tour
from app.models.User import User

def generate_reference():
    """Generate a unique booking reference."""
    return f"BK{uuid.uuid4().hex[:8].upper()}"

def add_demo_bookings():
    """Add demo bookings for existing users."""
    app = create_app()
    
    with app.app_context():
        # Get all users
        users = User.query.all()
        if not users:
            print("No users found in the database. Please create users first.")
            return
        
        # Get all tours
        tours = Tour.query.filter_by(is_active=True).all()
        if not tours:
            print("No active tours found in the database. Please create tours first.")
            return
        
        print(f" Found {len(users)} users and {len(tours)} tours")
        
        # Sample booking data templates (will be customized per user)
        booking_templates = [
            {
                'num_people': 2,
                'special_requests': 'Vegetarian meals preferred. Need wheelchair accessibility.',
                'payment_status': 'paid',
                'payment_method': 'momo',
                'payment_reference': 'MTN123456789',
                'booking_date': date.today() + timedelta(days=15),
                'booking_time': time(9, 0),  # 9:00 AM
                'total_amount': Decimal('450000.00')
            },
            {
                'num_people': 4,
                'special_requests': 'Family with 2 children (ages 8 and 12). Looking for educational experience.',
                'payment_status': 'pending',
                'payment_method': 'card',
                'payment_reference': None,
                'booking_date': date.today() + timedelta(days=30),
                'booking_time': time(8, 30),  # 8:30 AM
                'total_amount': Decimal('1200000.00')
            },
            {
                'num_people': 1,
                'special_requests': 'Solo traveler. Interested in photography. Can I bring my camera equipment?',
                'payment_status': 'paid',
                'payment_method': 'bank',
                'payment_reference': 'BANK987654321',
                'booking_date': date.today() + timedelta(days=7),
                'booking_time': time(10, 0),  # 10:00 AM
                'total_amount': Decimal('280000.00')
            },
            {
                'num_people': 3,
                'special_requests': 'Group of friends celebrating birthday. Can you arrange a special cake?',
                'payment_status': 'cancelled',
                'payment_method': 'momo',
                'payment_reference': 'MTN987654321',
                'booking_date': date.today() + timedelta(days=5),
                'booking_time': time(7, 0),  # 7:00 AM
                'total_amount': Decimal('750000.00'),
                'cancellation_reason': 'plans_changed',
                'cancellation_notes': 'Friend got sick, had to postpone the trip.'
            },
            {
                'num_people': 6,
                'special_requests': 'Corporate team building event. Need meeting space for 2 hours.',
                'payment_status': 'paid',
                'payment_method': 'card',
                'payment_reference': 'CARD123456789',
                'booking_date': date.today() + timedelta(days=45),
                'booking_time': time(11, 0),  # 11:00 AM
                'total_amount': Decimal('1800000.00')
            },
            {
                'num_people': 2,
                'special_requests': 'Honeymoon couple. Looking for romantic experience.',
                'payment_status': 'pending',
                'payment_method': None,
                'payment_reference': None,
                'booking_date': date.today() + timedelta(days=60),
                'booking_time': time(6, 30),  # 6:30 AM
                'total_amount': Decimal('600000.00')
            },
            {
                'num_people': 1,
                'special_requests': 'Backpacker on budget. Any discounts available?',
                'payment_status': 'paid',
                'payment_method': 'momo',
                'payment_reference': 'MTN456789123',
                'booking_date': date.today() + timedelta(days=3),
                'booking_time': time(14, 0),  # 2:00 PM
                'total_amount': Decimal('150000.00')
            },
            {
                'num_people': 5,
                'special_requests': 'Family with elderly parents. Need comfortable transportation.',
                'payment_status': 'cancelled',
                'payment_method': 'bank',
                'payment_reference': 'BANK123789456',
                'booking_date': date.today() + timedelta(days=20),
                'booking_time': time(9, 30),  # 9:30 AM
                'total_amount': Decimal('900000.00'),
                'cancellation_reason': 'found_better',
                'cancellation_notes': 'Found a better deal with another company.'
            }
        ]
        
        bookings_created = 0
        
        # Create bookings for each user
        for user in users:
            print(f"📝 Creating bookings for user: {user.username}")
            
            # Create 2-3 bookings per user
            for i in range(min(3, len(booking_templates))):
                booking_data = booking_templates[i].copy()
                
                # Rotate through tours
                tour = tours[i % len(tours)]
                
                # Use actual user information
                full_name = f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else user.username
                email = user.email
                phone = user.phone if user.phone else '+256700000000'  # Default phone if not set
                
                # Create the booking
                booking = Booking(
                    reference=generate_reference(),
                    user_id=user.id,
                    tour_id=tour.id,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    booking_date=booking_data['booking_date'],
                    booking_time=booking_data['booking_time'],
                    num_people=booking_data['num_people'],
                    special_requests=booking_data['special_requests'],
                    total_amount=booking_data['total_amount'],
                    payment_method=booking_data['payment_method'],
                    payment_status=booking_data['payment_status'],
                    payment_reference=booking_data['payment_reference'],
                    payment_details=f"Demo booking for {tour.title}",
                    order_tracking_id=f"TRK{uuid.uuid4().hex[:8].upper()}"
                )
                
                # Add cancellation details if cancelled
                if booking_data['payment_status'] == 'cancelled':
                    booking.cancellation_reason = booking_data['cancellation_reason']
                    booking.cancellation_notes = booking_data['cancellation_notes']
                    booking.cancelled_at = datetime.utcnow() - timedelta(days=2)
                
                try:
                    db.session.add(booking)
                    bookings_created += 1
                    print(f"   ✅ Created booking {booking.reference} for {tour.title}")
                except Exception as e:
                    print(f"   ❌ Error creating booking: {e}")
                    db.session.rollback()
        
        # Commit all changes
        try:
            db.session.commit()
            print(f"\n🎉 Successfully created {bookings_created} demo bookings!")
            print(f"📊 Booking status breakdown:")
            
            # Show statistics
            total_bookings = Booking.query.count()
            paid_bookings = Booking.query.filter_by(payment_status='paid').count()
            pending_bookings = Booking.query.filter_by(payment_status='pending').count()
            cancelled_bookings = Booking.query.filter_by(payment_status='cancelled').count()
            
            print(f"   Total: {total_bookings}")
            print(f"   Paid: {paid_bookings}")
            print(f"   Pending: {pending_bookings}")
            print(f"   Cancelled: {cancelled_bookings}")
            
        except Exception as e:
            print(f"❌ Error committing bookings: {e}")
            db.session.rollback()

def main():
    """Main function to run the script."""
    print("🚀 Starting demo bookings creation...")
    add_demo_bookings()
    print("✨ Demo bookings script completed!")

if __name__ == '__main__':
    main() 