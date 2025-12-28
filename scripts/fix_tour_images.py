#!/usr/bin/env python3
"""
Simple script to fix tour images in the database
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.Tour import Tour

def fix_tour_images():
    """Update existing tours with proper image filenames"""
    app = create_app()
    
    with app.app_context():
        print("Fixing tour images...")
        print("=" * 60)
        
        tours = Tour.query.all()
        
        if not tours:
            print(" No tours found in database!")
            return
        
        print(f"Found {len(tours)} tours in database")
        print()
        
        # Map tour titles to image filenames
        image_mapping = {
            '3-Day Zanzibar Beach Escape': 'zanzibar.jpeg',
            'Kalangala – Brovad Sands Lodge': 'kalangala.jpg',
            'Western Uganda Safari': 'westernUganda.jpg',
            '5-Day Ugandan Safari': 'victoriafalls.jpeg'
        }
        
        updated_count = 0
        for tour in tours:
            print(f"Tour: {tour.title}")
            print(f"   Current image: {tour.image or 'None'}")
            
            if tour.title in image_mapping:
                new_image = image_mapping[tour.title]
                tour.image = new_image
                updated_count += 1
                print(f"    Updated to: {new_image}")
                
                # Check if file exists
                image_path = Path(f"app/static/images/tours/{new_image}")
                if image_path.exists():
                    print(f"    File exists: {image_path}")
                else:
                    print(f"    File missing: {image_path}")
            else:
                print(f"    No mapping found for this tour")
            
            print("-" * 60)
        
        if updated_count > 0:
            db.session.commit()
            print(f"\nSuccessfully updated {updated_count} tours!")
            print("Please refresh your tours page to see the changes.")
        else:
            print("\nNo tours were updated.")

if __name__ == '__main__':
    fix_tour_images() 