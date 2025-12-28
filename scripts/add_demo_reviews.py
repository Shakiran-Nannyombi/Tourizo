#!/usr/bin/env python
"""Add demo reviews for tours using existing users"""
from app import create_app, db
from app.models.Review import Review
from app.models.Tour import Tour
from app.models.User import User
from datetime import datetime, timedelta
import random

app = create_app()

# Sample review comments for different ratings
review_templates = {
    5: [
        "Absolutely amazing experience! The tour exceeded all my expectations. Highly recommended!",
        "This was the trip of a lifetime! Everything was perfectly organized and the guides were fantastic.",
        "Outstanding tour! The scenery was breathtaking and the service was impeccable.",
        "Best vacation ever! I would do this tour again in a heartbeat. Five stars all the way!",
        "Incredible experience from start to finish. The attention to detail was impressive.",
    ],
    4: [
        "Great tour overall! Had a wonderful time and would recommend it to friends.",
        "Really enjoyed this experience. A few minor issues but nothing major.",
        "Very good tour with excellent guides. Would definitely consider booking again.",
        "Solid experience with beautiful locations. Well worth the price.",
        "Had a fantastic time! The itinerary was well-planned and enjoyable.",
    ],
    3: [
        "Good tour but there's room for improvement. Overall satisfied with the experience.",
        "Decent experience. Some parts were great, others could be better organized.",
        "Average tour. Met most expectations but nothing extraordinary.",
        "It was okay. Some highlights but also some disappointments.",
        "Fair experience. Good value for money but could be enhanced.",
    ],
    2: [
        "Below expectations. Several issues with organization and timing.",
        "Not what I hoped for. Some aspects were good but many problems.",
        "Disappointing experience. Would not recommend at this price point.",
    ],
    1: [
        "Very disappointing. Multiple issues throughout the tour.",
        "Poor experience. Would not recommend to others.",
    ],
}

with app.app_context():
    # Get all users and tours
    users = User.query.all()
    tours = Tour.query.all()
    
    if not users:
        print("No users found in database. Please import users first.")
        exit(1)
    
    if not tours:
        print("No tours found in database. Please import tours first.")
        exit(1)
    
    # Check if reviews already exist
    existing_count = Review.query.count()
    if existing_count > 0:
        print(f"Database already has {existing_count} review(s).")
        response = input("Do you want to clear existing reviews and import demo data? (yes/no): ")
        if response.lower() != 'yes':
            print("Import cancelled.")
            exit(0)
        
        # Clear existing reviews
        Review.query.delete()
        db.session.commit()
        print("Cleared existing reviews")
    
    print(f"\nGenerating demo reviews...")
    print(f"Found {len(users)} users and {len(tours)} tours\n")
    
    reviews_created = 0
    
    # Create 2-4 reviews per tour from different users
    for tour in tours:
        num_reviews = random.randint(2, 4)
        selected_users = random.sample(users, min(num_reviews, len(users)))
        
        for user in selected_users:
            # Generate rating (weighted towards higher ratings)
            rating = random.choices(
                [5, 4, 3, 2, 1],
                weights=[50, 30, 15, 4, 1]  # More likely to get 4-5 stars
            )[0]
            
            # Select a random comment for this rating
            comment = random.choice(review_templates[rating])
            
            # Create review with random date in the past 60 days
            days_ago = random.randint(1, 60)
            created_date = datetime.utcnow() - timedelta(days=days_ago)
            
            review = Review(
                rating=rating,
                comment=comment,
                reviewer_name=user.username,
                reviewer_email=user.email,
                is_verified=True,  # Mark as verified since they're real users
                is_approved=True,  # Auto-approve demo reviews
                created_at=created_date,
                tour_id=tour.id,
                user_id=user.id
            )
            
            db.session.add(review)
            reviews_created += 1
        
        print(f"Added {num_reviews} reviews for: {tour.title}")
    
    db.session.commit()
    
    print(f"\nSuccessfully created {reviews_created} demo reviews!")
    
    # Show review statistics
    print("\n" + "=" * 80)
    print("REVIEW STATISTICS")
    print("=" * 80)
    
    for rating in [5, 4, 3, 2, 1]:
        count = Review.query.filter_by(rating=rating).count()
        stars = "⭐" * rating
        print(f"{stars} ({rating} stars): {count} reviews")
    
    print("\n" + "=" * 80)
    print("REVIEWS BY TOUR")
    print("=" * 80)
    
    for tour in tours:
        review_count = Review.query.filter_by(tour_id=tour.id).count()
        avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(tour_id=tour.id).scalar()
        avg_rating = round(avg_rating, 1) if avg_rating else 0
        print(f"{tour.title:40} | {review_count} reviews | Avg: {avg_rating} ⭐")
    
    print("=" * 80)
