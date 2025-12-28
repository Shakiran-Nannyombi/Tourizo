#!/usr/bin/env python3
"""
Script to add image galleries to existing tours
This script will add multiple images to each tour's gallery
"""

import sys
import os
import json
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.Tour import Tour

def add_image_galleries():
    """Add image galleries to existing tours"""
    
    # Define image galleries for each tour
    tour_galleries = {
        'Serengeti Wildlife Safari': [
            'segerenti.jpeg',
            'masaimara.jpeg',
            'camptown.jpeg',
            'uganda.jpg'
        ],
        'Kilimanjaro Summit Trek': [
            'kilimanjaro.jpeg',
            'camptown.jpeg',
            'westernUganda.jpg'
        ],
        'Victoria Falls Adventure': [
            'victoriafalls.jpeg',
            'camptown.jpeg',
            'uganda.jpg'
        ],
        'Masai Mara Safari Experience': [
            'masaimara.jpeg',
            'segerenti.jpeg',
            'camptown.jpeg'
        ],
        'Sahara Desert Expedition': [
            'sahara.jpeg',
            'camptown.jpeg',
            'uganda.jpg'
        ],
        'Uganda Gorilla Trekking': [
            'gorilla.jpeg',
            'westernUganda.jpg',
            'uganda.jpg',
            'camptown.jpeg'
        ],
        'Western Uganda Adventure': [
            'westernUganda.jpg',
            'uganda.jpg',
            'gorilla.jpeg',
            'camptown.jpeg'
        ],
        'Kalangala Island Getaway': [
            'kalangala.jpg',
            'zanzibar.jpeg',
            'camptown.jpeg'
        ],
        'Zanzibar Beach and Culture Tour': [
            'zanzibar.jpeg',
            'kalangala.jpg',
            'camptown.jpeg',
            'uganda.jpg'
        ]
    }
    
    updated_count = 0
    
    for tour_title, gallery_images in tour_galleries.items():
        tour = Tour.query.filter_by(title=tour_title).first()
        
        if tour:
            # Convert gallery images to JSON string
            tour.image_gallery = json.dumps(gallery_images)
            updated_count += 1
            print(f"Updated gallery for: {tour_title} ({len(gallery_images)} images)")
        else:
            print(f"Tour not found: {tour_title}")
    
    # Commit changes
    db.session.commit()
    print(f"\nSuccessfully updated {updated_count} tours with image galleries!")

def main():
    """Main function"""
    app = create_app()
    
    with app.app_context():
        print("Adding image galleries to tours...")
        add_image_galleries()
        print("Image gallery update completed!")

if __name__ == '__main__':
    main() 