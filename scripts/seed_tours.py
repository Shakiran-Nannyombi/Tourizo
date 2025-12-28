#!/usr/bin/env python3
"""
Database seeding script for adding sample tours to Tourizo
Run this script to populate your database with sample tour data
"""

import sys
import os
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.Tour import Tour, TourItineraryDay
from app.models.Category import Category

def create_categories():
    """Create sample categories if they don't exist"""
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
        categories[cat_data['name']] = category
    
    db.session.commit()
    return categories

def create_sample_tours(categories):
    """Create sample tours"""
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
            'title': 'Victoria Falls Adventure',
            'short_description': 'Discover the magnificent Victoria Falls and surrounding adventures',
            'description': 'Experience the awe-inspiring Victoria Falls, one of the Seven Natural Wonders of the World. This tour combines waterfall viewing with thrilling activities like white-water rafting, helicopter flights, and wildlife encounters.',
            'destination': 'Victoria Falls, Zambia/Zimbabwe',
            'departure_location': 'Livingstone, Zambia',
            'category_id': categories['Adventure Tours'].id,
            'price': 1200.00,
            'duration': 5,
            'duration_type': 'Days',
            'max_participants': 15,
            'min_participants': 2,
            'difficulty_level': 'Medium',
            'image': 'victoriafalls.jpeg',
            'inclusions': 'Accommodation, meals, activities, guide, park fees, transportation',
            'exclusions': 'International flights, optional activities, personal expenses',
            'itinerary': 'Day 1: Arrival and Victoria Falls tour\nDay 2: White-water rafting\nDay 3: Helicopter flight over falls\nDay 4: Safari in Mosi-oa-Tunya National Park\nDay 5: Departure',
            'available_from': datetime.now().date(),
            'available_to': (datetime.now() + timedelta(days=365)).date(),
            'is_active': True,
            'is_featured': True,
            'meta_title': 'Victoria Falls Adventure - Experience the Smoke that Thunders',
            'meta_description': 'Discover Victoria Falls with thrilling adventures and wildlife encounters'
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
        },
        {
            'title': 'Western Uganda Adventure',
            'short_description': 'Explore the diverse landscapes and wildlife of Western Uganda',
            'description': 'Discover the natural wonders of Western Uganda, from the stunning Lake Bunyonyi to the wildlife-rich Queen Elizabeth National Park. This adventure combines scenic beauty with incredible wildlife viewing opportunities.',
            'destination': 'Western Uganda',
            'departure_location': 'Kampala, Uganda',
            'category_id': categories['Adventure Tours'].id,
            'price': 1400.00,
            'duration': 7,
            'duration_type': 'Days',
            'max_participants': 10,
            'min_participants': 2,
            'difficulty_level': 'Easy',
            'image': 'westernUganda.jpg',
            'inclusions': 'Accommodation, meals, activities, guide, park fees, transportation',
            'exclusions': 'International flights, personal expenses, tips, travel insurance',
            'itinerary': 'Day 1: Kampala to Lake Bunyonyi\nDay 2: Lake activities and relaxation\nDay 3: Transfer to Queen Elizabeth NP\nDay 4-5: Game drives and boat safari\nDay 6: Chimpanzee tracking\nDay 7: Return to Kampala',
            'available_from': datetime.now().date(),
            'available_to': (datetime.now() + timedelta(days=365)).date(),
            'is_active': True,
            'is_featured': False,
            'meta_title': 'Western Uganda Adventure - Discover Uganda\'s Natural Wonders',
            'meta_description': 'Explore the diverse landscapes and wildlife of Western Uganda'
        },
        {
            'title': 'Kalangala Island Getaway',
            'short_description': 'Relax on the beautiful islands of Lake Victoria',
            'description': 'Escape to the pristine islands of Kalangala in Lake Victoria for a peaceful beach getaway. Enjoy white sandy beaches, crystal clear waters, and authentic island life away from the hustle and bustle of the mainland.',
            'destination': 'Kalangala Islands, Uganda',
            'departure_location': 'Entebbe, Uganda',
            'category_id': categories['Beach Holidays'].id,
            'price': 800.00,
            'duration': 4,
            'duration_type': 'Days',
            'max_participants': 15,
            'min_participants': 2,
            'difficulty_level': 'Easy',
            'image': 'kalangala.jpg',
            'inclusions': 'Island accommodation, meals, boat transfers, beach activities',
            'exclusions': 'International flights, personal expenses, tips, travel insurance',
            'itinerary': 'Day 1: Boat transfer to Kalangala\nDay 2: Beach relaxation and water activities\nDay 3: Island exploration and fishing\nDay 4: Return to mainland',
            'available_from': datetime.now().date(),
            'available_to': (datetime.now() + timedelta(days=365)).date(),
            'is_active': True,
            'is_featured': False,
            'meta_title': 'Kalangala Island Getaway - Paradise on Lake Victoria',
            'meta_description': 'Escape to the beautiful Kalangala islands for a perfect beach holiday'
        },
        {
            'title': 'Zanzibar Beach and Culture Tour',
            'short_description': 'Discover the stunning beaches and rich culture of Zanzibar',
            'description': 'Experience the best of Zanzibar with its pristine beaches, vibrant culture, and rich history. This tour combines relaxation on the beach with cultural excursions to Stone Town and spice plantations.',
            'destination': 'Zanzibar, Tanzania',
            'departure_location': 'Stone Town, Zanzibar',
            'category_id': categories['Beach Holidays'].id,
            'price': 1100.00,
            'duration': 6,
            'duration_type': 'Days',
            'max_participants': 20,
            'min_participants': 2,
            'difficulty_level': 'Easy',
            'image': 'zanzibar.jpeg',
            'inclusions': 'Accommodation, meals, cultural tours, beach activities, guide',
            'exclusions': 'International flights, personal expenses, tips, travel insurance',
            'itinerary': 'Day 1: Arrival in Stone Town\nDay 2: Spice plantation tour\nDay 3-4: Beach relaxation at Nungwi\nDay 5: Cultural tour of Stone Town\nDay 6: Departure',
            'available_from': datetime.now().date(),
            'available_to': (datetime.now() + timedelta(days=365)).date(),
            'is_active': True,
            'is_featured': True,
            'meta_title': 'Zanzibar Beach and Culture Tour - Paradise Awaits',
            'meta_description': 'Explore the stunning beaches and rich culture of Zanzibar'
        }
    ]
    
    for tour_data in tours_data:
        # Check if tour already exists
        existing_tour = Tour.query.filter_by(title=tour_data['title']).first()
        if not existing_tour:
            tour = Tour(**tour_data)
            db.session.add(tour)
            print(f"Added tour: {tour_data['title']}")
        else:
            print(f"Tour already exists: {tour_data['title']}")
    
    db.session.commit()

def create_sample_itineraries(tours):
    """Create sample itinerary days for each tour"""
    for tour in tours:
        if tour.title == 'Serengeti Wildlife Safari':
            days = [
                (1, 'Arrival in Arusha', 'Arrive at Kilimanjaro Airport and transfer to your hotel in Arusha. Meet your guide and fellow travelers for a welcome dinner.'),
                (2, 'Arusha to Serengeti', 'Early morning departure to Serengeti National Park. Game drive en route to your luxury tented camp.'),
                (3, 'Full Day Serengeti Safari', 'Full day game drives in the Serengeti. Morning and afternoon drives with lunch at the camp.'),
                (4, 'Serengeti to Ngorongoro', 'Morning game drive, then travel to Ngorongoro Conservation Area. Overnight at crater rim lodge.'),
                (5, 'Ngorongoro Crater', 'Descend into the crater for a full day of game viewing. Picnic lunch on the crater floor.'),
                (6, 'Cultural Experience', 'Visit a local Maasai village and learn about traditional culture. Afternoon at leisure.'),
                (7, 'Departure', 'Morning at leisure, then transfer to Kilimanjaro Airport for your departure flight.')
            ]
        elif tour.title == 'Kilimanjaro Summit Trek':
            days = [
                (1, 'Arrival in Moshi', 'Arrive in Moshi and meet your trek leader for a briefing and gear check.'),
                (2, 'Machame Gate to Machame Camp', 'Begin your trek through lush rainforest to Machame Camp.'),
                (3, 'Machame Camp to Shira Camp', 'Ascend through moorland to Shira Camp with stunning views.'),
                (4, 'Shira Camp to Barranco Camp', 'Trek across the Shira Plateau and up to Barranco Camp.'),
                (5, 'Barranco Camp to Karanga Camp', 'Climb the Barranco Wall and descend to Karanga Valley.'),
                (6, 'Karanga Camp to Barafu Camp', 'Hike to Barafu Camp, your base for the summit attempt.'),
                (7, 'Summit Day', 'Midnight start for the summit push to Uhuru Peak, then descend to Mweka Camp.'),
                (8, 'Descent and Departure', 'Finish your descent and return to Moshi for celebration and departure.')
            ]
        elif tour.title == 'Victoria Falls Adventure':
            days = [
                (1, 'Arrival and Victoria Falls Tour', 'Arrive in Livingstone and enjoy a guided tour of Victoria Falls.'),
                (2, 'White-water Rafting', 'Experience thrilling white-water rafting on the Zambezi River.'),
                (3, 'Helicopter Flight', 'Take a scenic helicopter flight over the falls and surrounding area.'),
                (4, 'Safari in Mosi-oa-Tunya', 'Go on a wildlife safari in Mosi-oa-Tunya National Park.'),
                (5, 'Departure', 'Transfer to the airport for your onward journey.')
            ]
        elif tour.title == 'Masai Mara Safari Experience':
            days = [
                (1, 'Arrival in Nairobi', 'Arrive in Nairobi and transfer to your hotel.'),
                (2, 'Transfer to Masai Mara', 'Drive to Masai Mara with scenic stops along the way.'),
                (3, 'Full Day Game Drives', 'Enjoy morning and afternoon game drives in the Masai Mara.'),
                (4, 'More Game Drives', 'Another day of wildlife viewing and photography.'),
                (5, 'Maasai Village Visit', 'Visit a local Maasai village to learn about their culture.'),
                (6, 'Return to Nairobi', 'Drive back to Nairobi for your departure.')
            ]
        elif tour.title == 'Sahara Desert Expedition':
            days = [
                (1, 'Marrakech to Merzouga', 'Travel from Marrakech to the edge of the Sahara in Merzouga.'),
                (2, 'Camel Trek into Desert', 'Begin your camel trek and camp under the stars.'),
                (3, 'Desert Exploration', 'Explore sand dunes and oases, visit a Berber family.'),
                (4, 'Return to Marrakech', 'Ride back to Merzouga and transfer to Marrakech.')
            ]
        elif tour.title == 'Uganda Gorilla Trekking':
            days = [
                (1, 'Arrival in Kampala', 'Arrive in Kampala and meet your guide.'),
                (2, 'Transfer to Bwindi', 'Drive to Bwindi Impenetrable Forest, home of the gorillas.'),
                (3, 'Gorilla Trekking', 'Trek through the forest to observe mountain gorillas.'),
                (4, 'Optional Second Trek', 'Choose a second trek or visit a local community.'),
                (5, 'Return to Kampala', 'Drive back to Kampala for your departure.')
            ]
        elif tour.title == 'Western Uganda Adventure':
            days = [
                (1, 'Kampala to Lake Bunyonyi', 'Travel to Lake Bunyonyi and enjoy lake activities.'),
                (2, 'Lake Activities', 'Canoeing, swimming, and relaxation at the lake.'),
                (3, 'Transfer to Queen Elizabeth NP', 'Drive to Queen Elizabeth National Park.'),
                (4, 'Game Drives', 'Morning and afternoon game drives in the park.'),
                (5, 'Boat Safari', 'Take a boat safari on the Kazinga Channel.'),
                (6, 'Chimpanzee Tracking', 'Track chimpanzees in the Kyambura Gorge.'),
                (7, 'Return to Kampala', 'Drive back to Kampala for your departure.')
            ]
        elif tour.title == 'Kalangala Island Getaway':
            days = [
                (1, 'Boat Transfer to Kalangala', 'Take a boat to Kalangala Island and check in to your hotel.'),
                (2, 'Beach Relaxation', 'Enjoy the beaches and water activities.'),
                (3, 'Island Exploration', 'Explore the island, visit local villages and forests.'),
                (4, 'Return to Mainland', 'Boat transfer back to the mainland for departure.')
            ]
        elif tour.title == 'Zanzibar Beach and Culture Tour':
            days = [
                (1, 'Arrival in Stone Town', 'Arrive in Zanzibar and explore historic Stone Town.'),
                (2, 'Spice Plantation Tour', 'Visit a spice plantation and learn about Zanzibar’s spices.'),
                (3, 'Beach Relaxation', 'Relax on the white sand beaches of Nungwi.'),
                (4, 'More Beach Time', 'Enjoy more beach activities or optional excursions.'),
                (5, 'Cultural Tour', 'Take a cultural tour of Stone Town and visit local markets.'),
                (6, 'Departure', 'Transfer to the airport for your departure.')
            ]
        else:
            days = []
        for day, title, desc in days:
            db.session.add(TourItineraryDay(tour_id=tour.id, day=day, title=title, description=desc))
    db.session.commit()

def main():
    """Main function to seed the database"""
    app = create_app()
    
    with app.app_context():
        print("Starting database seeding...")
        
        # Create categories
        print("Creating categories...")
        categories = create_categories()
        
        # Create tours
        print("Creating sample tours...")
        create_sample_tours(categories)
        
        tours = Tour.query.all()
        print("Creating sample itineraries...")
        create_sample_itineraries(tours)
        
        print("Database seeding completed successfully!")
        print(f"Created {len(categories)} categories")
        
        # Count tours
        tour_count = Tour.query.count()
        print(f"Total tours in database: {tour_count}")

if __name__ == '__main__':
    main() 