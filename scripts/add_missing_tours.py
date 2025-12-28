#!/usr/bin/env python3
"""
Script to add missing tours from seed_tours.py to the database
"""

import sys
import os
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.Tour import Tour
from app.models.Category import Category

def get_or_create_categories():
    """Get existing categories or create them if they don't exist"""
    categories_data = [
        {'name': 'Adventure Tours', 'description': 'Thrilling outdoor adventures and expeditions'},
        {'name': 'Cultural Tours', 'description': 'Immerse yourself in local culture and traditions'},
        {'name': 'Wildlife Safaris', 'description': 'Explore wildlife in their natural habitats'},
        {'name': 'Beach Holidays', 'description': 'Relaxing beach getaways and coastal adventures'},
        {'name': 'Mountain Trekking', 'description': 'Challenging mountain hikes and climbs'},
        {'name': 'City Tours', 'description': 'Urban exploration and city sightseeing'},
        {'name': 'Historical Tours', 'description': 'Journey through history and heritage sites'},
        {'name': 'Luxury Tours', 'description': 'Premium travel experiences with high-end amenities'}
    ]
    
    categories = {}
    for cat_data in categories_data:
        category = Category.query.filter_by(name=cat_data['name']).first()
        if not category:
            category = Category(**cat_data)
            db.session.add(category)
            db.session.flush()  # Get the ID
            print(f"Created category: {cat_data['name']}")
        else:
            print(f"Found existing category: {cat_data['name']}")
        categories[cat_data['name']] = category
    
    db.session.commit()
    return categories

def add_missing_tours(categories):
    """Add missing tours from the seeder"""
    tours_data = [
        {
            'title': 'Serengeti Wildlife Safari',
            'short_description': 'Experience the incredible wildlife of the Serengeti plains',
            'description': 'Embark on an unforgettable journey through the Serengeti National Park, home to the Big Five and the annual wildebeest migration. This safari offers close encounters with lions, elephants, giraffes, and countless other species in their natural habitat.',
            'destination': 'Serengeti, Tanzania',
            'departure_location': 'Arusha, Tanzania',
            'category_id': categories['Wildlife Safaris'].id,
            'price': 2500.00,
            'duration': 7,
            'duration_type': 'Days',
            'max_participants': 12,
            'min_participants': 2,
            'difficulty_level': 'Easy',
            'image': 'segerenti.jpeg',
            'inclusions': 'Accommodation, meals, game drives, professional guide, park fees, transportation',
            'exclusions': 'International flights, personal expenses, tips, travel insurance',
            'itinerary': 'Day 1: Arrival in Arusha\nDay 2-3: Central Serengeti game drives\nDay 4-5: Northern Serengeti migration viewing\nDay 6: Ngorongoro Crater\nDay 7: Return to Arusha',
            'available_from': datetime.now().date(),
            'available_to': (datetime.now() + timedelta(days=365)).date(),
            'is_active': True,
            'is_featured': True,
            'meta_title': 'Serengeti Wildlife Safari - Experience the Big Five',
            'meta_description': 'Join our Serengeti safari for unforgettable wildlife encounters in Tanzania'
        },
        {
            'title': 'Kilimanjaro Summit Trek',
            'short_description': 'Conquer Africa\'s highest peak on this challenging trek',
            'description': 'Challenge yourself to reach the summit of Mount Kilimanjaro, Africa\'s highest peak at 5,895 meters. This trek takes you through diverse ecosystems from rainforest to alpine desert, culminating in the stunning Uhuru Peak.',
            'destination': 'Mount Kilimanjaro, Tanzania',
            'departure_location': 'Moshi, Tanzania',
            'category_id': categories['Mountain Trekking'].id,
            'price': 1800.00,
            'duration': 8,
            'duration_type': 'Days',
            'max_participants': 8,
            'min_participants': 1,
            'difficulty_level': 'Hard',
            'image': 'kilimanjaro.jpeg',
            'inclusions': 'Accommodation, meals, guide, porters, park fees, equipment rental',
            'exclusions': 'International flights, personal gear, tips, travel insurance',
            'itinerary': 'Day 1: Arrival in Moshi\nDay 2: Machame Gate to Machame Camp\nDay 3: Machame Camp to Shira Camp\nDay 4: Shira Camp to Barranco Camp\nDay 5: Barranco Camp to Karanga Camp\nDay 6: Karanga Camp to Barafu Camp\nDay 7: Summit day\nDay 8: Descent and return',
            'available_from': datetime.now().date(),
            'available_to': (datetime.now() + timedelta(days=365)).date(),
            'is_active': True,
            'is_featured': False,
            'meta_title': 'Kilimanjaro Summit Trek - Conquer Africa\'s Highest Peak',
            'meta_description': 'Experience the ultimate challenge with our Kilimanjaro summit trek'
        },
        {
            'title': 'Masai Mara Safari Experience',
            'short_description': 'Explore Kenya\'s most famous wildlife reserve',
            'description': 'Journey to the Masai Mara, Kenya\'s premier wildlife destination. Witness the spectacular wildebeest migration, spot the Big Five, and experience authentic Maasai culture in this unforgettable safari adventure.',
            'destination': 'Masai Mara, Kenya',
            'departure_location': 'Nairobi, Kenya',
            'category_id': categories['Wildlife Safaris'].id,
            'price': 1600.00,
            'duration': 6,
            'duration_type': 'Days',
            'max_participants': 10,
            'min_participants': 2,
            'difficulty_level': 'Easy',
            'image': 'masaimara.jpeg',
            'inclusions': 'Luxury tented accommodation, meals, game drives, Maasai village visit, guide',
            'exclusions': 'International flights, personal expenses, tips, travel insurance',
            'itinerary': 'Day 1: Arrival in Nairobi\nDay 2: Transfer to Masai Mara\nDay 3-4: Full day game drives\nDay 5: Maasai village visit\nDay 6: Return to Nairobi',
            'available_from': datetime.now().date(),
            'available_to': (datetime.now() + timedelta(days=365)).date(),
            'is_active': True,
            'is_featured': False,
            'meta_title': 'Masai Mara Safari - Kenya\'s Premier Wildlife Experience',
            'meta_description': 'Experience the magic of Masai Mara with our exclusive safari packages'
        },
        {
            'title': 'Sahara Desert Expedition',
            'short_description': 'Cross the vast Sahara Desert on camelback',
            'description': 'Embark on an epic journey across the Sahara Desert, the world\'s largest hot desert. Experience traditional Berber hospitality, sleep under the stars, and witness breathtaking desert landscapes and ancient oases.',
            'destination': 'Sahara Desert, Morocco',
            'departure_location': 'Marrakech, Morocco',
            'category_id': categories['Adventure Tours'].id,
            'price': 900.00,
            'duration': 4,
            'duration_type': 'Days',
            'max_participants': 12,
            'min_participants': 2,
            'difficulty_level': 'Medium',
            'image': 'sahara.jpeg',
            'inclusions': 'Camel trek, desert camp accommodation, meals, guide, transportation',
            'exclusions': 'International flights, personal expenses, tips, travel insurance',
            'itinerary': 'Day 1: Marrakech to Merzouga\nDay 2: Camel trek into desert\nDay 3: Desert exploration and camping\nDay 4: Return to Marrakech',
            'available_from': datetime.now().date(),
            'available_to': (datetime.now() + timedelta(days=365)).date(),
            'is_active': True,
            'is_featured': False,
            'meta_title': 'Sahara Desert Expedition - Cross the World\'s Largest Desert',
            'meta_description': 'Experience the magic of the Sahara Desert with our camel trek expedition'
        },
        {
            'title': 'Uganda Gorilla Trekking',
            'short_description': 'Encounter mountain gorillas in their natural habitat',
            'description': 'Experience one of the most intimate wildlife encounters on Earth - trekking to see mountain gorillas in Uganda\'s Bwindi Impenetrable Forest. This once-in-a-lifetime experience brings you face-to-face with these gentle giants.',
            'destination': 'Bwindi Forest, Uganda',
            'departure_location': 'Kampala, Uganda',
            'category_id': categories['Wildlife Safaris'].id,
            'price': 2800.00,
            'duration': 5,
            'duration_type': 'Days',
            'max_participants': 8,
            'min_participants': 1,
            'difficulty_level': 'Medium',
            'image': 'gorilla.jpg',
            'inclusions': 'Gorilla permits, accommodation, meals, guide, transportation, park fees',
            'exclusions': 'International flights, personal expenses, tips, travel insurance',
            'itinerary': 'Day 1: Arrival in Kampala\nDay 2: Transfer to Bwindi\nDay 3: Gorilla trekking\nDay 4: Optional second trek or cultural visit\nDay 5: Return to Kampala',
            'available_from': datetime.now().date(),
            'available_to': (datetime.now() + timedelta(days=365)).date(),
            'is_active': True,
            'is_featured': True,
            'meta_title': 'Uganda Gorilla Trekking - Meet Mountain Gorillas Face-to-Face',
            'meta_description': 'Experience the magic of gorilla trekking in Uganda\'s Bwindi Forest'
        }
    ]
    
    added_count = 0
    for tour_data in tours_data:
        # Check if tour already exists
        existing_tour = Tour.query.filter_by(title=tour_data['title']).first()
        if not existing_tour:
            tour = Tour(**tour_data)
            db.session.add(tour)
            print(f"Added tour: {tour_data['title']}")
            added_count += 1
        else:
            print(f" Tour already exists: {tour_data['title']}")
    
    db.session.commit()
    return added_count

def main():
    """Main function"""
    app = create_app()
    
    with app.app_context():
        print("Adding missing tours from seeder...")
        print("=" * 60)
        
        # Get or create categories
        print("\nSetting up categories...")
        categories = get_or_create_categories()
        
        # Add missing tours
        print("\nAdding missing tours...")
        added_count = add_missing_tours(categories)
        
        # Show final status
        total_tours = Tour.query.count()
        print(f"\nCompleted!")
        print(f"Added {added_count} new tours")
        print(f"Total tours in database: {total_tours}")
        
        if added_count > 0:
            print("\nPlease refresh your tours page to see the new tours!")

if __name__ == '__main__':
    main() 