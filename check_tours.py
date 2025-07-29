#!/usr/bin/env python3
"""
Script to check all tours in the database and verify their image files
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.Tour import Tour

def check_tours():
    """Check all tours in the database and their image files"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking tours in database...")
        print("=" * 80)
        
        tours = Tour.query.all()
        
        if not tours:
            print(" No tours found in database!")
            return
        
        print(f"Found {len(tours)} tours in database")
        print()
        
        for tour in tours:
            print(f"Tour ID: {tour.id}")
            print(f"   Title: {tour.title}")
            print(f"   Destination: {tour.destination}")
            print(f"   Active: {'Yes' if tour.is_active else 'No'}")
            print(f"   Image field: {tour.image or 'None'}")
            
            if tour.image:
                # Check if image file exists
                image_path = Path(f"app/static/images/tours/{tour.image}")
                if image_path.exists():
                    print(f"   Image file: EXISTS ({image_path})")
                else:
                    print(f"   Image file: MISSING ({image_path})")
                    
                    # Check if file exists with different extension
                    base_name = image_path.stem
                    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                        alt_path = Path(f"app/static/images/tours/{base_name}{ext}")
                        if alt_path.exists():
                            print(f"    Found similar file: {alt_path}")
                            break
            else:
                print(f"   Image file: NO IMAGE SET")
            
            print(f"   Created: {tour.created_at}")
            print("-" * 80)

def reseed_database():
    """Reseed the database with sample tours"""
    app = create_app()
    
    with app.app_context():
        print("Reseeding database...")
        print("=" * 80)
        
        # Clear existing tours and related data
        from app.models.Booking import Booking
        from app.models.Review import Review
        from app.models.TourDate import TourDate
        from app.models.Tour import TourItineraryDay
        
        print("Clearing related data...")
        Booking.query.delete()
        Review.query.delete()
        TourDate.query.delete()
        TourItineraryDay.query.delete()
        Tour.query.delete()
        db.session.commit()
        print("Cleared all tour-related data")
        
        # Import and run the seeder
        try:
            from seed_tours import main as seed_main
            seed_main()
            print("Database reseeded successfully!")
        except Exception as e:
            print(f"Error reseeding database: {e}")
            return False
        
        return True

def update_existing_tours():
    """Update existing tours with proper image filenames"""
    app = create_app()
    
    with app.app_context():
        print("Updating existing tours with proper images...")
        print("=" * 80)
        
        tours = Tour.query.all()
        
        # Map tour titles to image filenames from seeder
        image_mapping = {
            'Serengeti Wildlife Safari': 'segerenti.jpeg',
            'Kilimanjaro Summit Trek': 'kilimanjaro.jpeg',
            'Victoria Falls Adventure': 'victoriafalls.jpeg',
            'Masai Mara Safari Experience': 'masaimara.jpeg',
            'Sahara Desert Expedition': 'sahara.jpeg',
            'Uganda Gorilla Trekking': 'gorilla.jpg',
            'Western Uganda Adventure': 'westernUganda.jpg',
            'Kalangala Island Getaway': 'kalangala.jpg',
            'Zanzibar Beach and Culture Tour': 'zanzibar.jpeg',
            '3-Day Zanzibar Beach Escape': 'zanzibar.jpeg',
            'Kalangala – Brovad Sands Lodge': 'kalangala.jpg',
            'Western Uganda Safari': 'westernUganda.jpg',
            '5-Day Ugandan Safari': 'victoriafalls.jpeg'
        }
        
        updated_count = 0
        for tour in tours:
            if tour.title in image_mapping:
                tour.image = image_mapping[tour.title]
                updated_count += 1
                print(f"Updated '{tour.title}' with image: {tour.image}")
            else:
                print(f"No image mapping found for: {tour.title}")
        
        if updated_count > 0:
            db.session.commit()
            print(f"\nUpdated {updated_count} tours with proper images!")
        else:
            print("\nNo tours were updated.")
        
        return updated_count > 0

def main():
    """Main function"""
    print(" Tour Database Checker")
    print("=" * 80)
    
    while True:
        print("\nOptions:")
        print("1. Check current tours in database")
        print("2. Reseed database with sample tours")
        print("3. Update existing tours with proper images")
        print("4. Check tours after changes")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            check_tours()
        elif choice == '2':
            if reseed_database():
                print("\nReseeding completed!")
            else:
                print("\nReseeding failed!")
        elif choice == '3':
            if update_existing_tours():
                print("\nTour updates completed!")
            else:
                print("\nTour updates failed!")
        elif choice == '4':
            print("\nChecking tours after changes...")
            check_tours()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == '__main__':
    main() 