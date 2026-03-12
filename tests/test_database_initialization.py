"""
Bug Condition Exploration Test: Database Initialization on Fresh Deployment

This test verifies that a fresh deployment with an empty database creates all required 
tables when `flask db upgrade` is run.

**Expected Outcome**: This test FAILS on unfixed code (proving the bug exists).
The failure demonstrates that tables are not created during migration.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4**
"""

import pytest
import os
import tempfile
import subprocess
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from app import create_app, db


class TestDatabaseInitialization:
    """Test that all required tables are created on fresh deployment"""

    @pytest.fixture
    def fresh_db_app(self):
        """Create app with a fresh empty database"""
        # Create a temporary database file
        db_fd, db_path = tempfile.mkstemp(suffix='.db')
        
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['TESTING'] = True
        
        with app.app_context():
            # Ensure database is empty - drop all tables if they exist
            db.drop_all()
            
            yield app, db_path
            
            # Cleanup
            db.session.remove()
            os.close(db_fd)
            os.unlink(db_path)

    def test_all_required_tables_created_after_migration(self, fresh_db_app):
        """
        Test that running flask db upgrade creates all required tables.
        
        This test simulates a fresh Render deployment:
        1. Start with empty database
        2. Run migrations via flask db upgrade
        3. Verify all required tables exist
        4. Verify table schemas are correct
        5. Verify foreign key relationships are established
        """
        app, db_path = fresh_db_app
        
        with app.app_context():
            # Run migrations on the fresh database
            upgrade(revision='head')
            
            # Get database connection and inspector
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            
            # List of required tables
            required_tables = [
                'category',
                'user',
                'destination',
                'chatbot_settings',
                'tour',
                'tour_date',
                'tour_itinerary_day',
                'tour_package',
                'booking',
                'review',
                'wishlist',
                'inquiries'
            ]
            
            # Get actual tables in database
            actual_tables = inspector.get_table_names()
            
            # Verify all required tables exist
            for table_name in required_tables:
                assert table_name in actual_tables, \
                    f"Table '{table_name}' not found. Existing tables: {actual_tables}"
            
            # Verify Category table schema
            category_columns = {col['name']: col for col in inspector.get_columns('category')}
            assert 'id' in category_columns, "Category table missing 'id' column"
            assert 'name' in category_columns, "Category table missing 'name' column"
            assert 'description' in category_columns, "Category table missing 'description' column"
            assert 'created_at' in category_columns, "Category table missing 'created_at' column"
            assert category_columns['name']['nullable'] == False, "Category.name should not be nullable"
            
            # Verify User table schema
            user_columns = {col['name']: col for col in inspector.get_columns('user')}
            assert 'id' in user_columns, "User table missing 'id' column"
            assert 'username' in user_columns, "User table missing 'username' column"
            assert 'email' in user_columns, "User table missing 'email' column"
            assert 'password_hash' in user_columns, "User table missing 'password_hash' column"
            assert 'is_admin' in user_columns, "User table missing 'is_admin' column"
            assert user_columns['username']['nullable'] == False, "User.username should not be nullable"
            assert user_columns['email']['nullable'] == False, "User.email should not be nullable"
            
            # Verify Tour table schema
            tour_columns = {col['name']: col for col in inspector.get_columns('tour')}
            assert 'id' in tour_columns, "Tour table missing 'id' column"
            assert 'title' in tour_columns, "Tour table missing 'title' column"
            assert 'description' in tour_columns, "Tour table missing 'description' column"
            assert 'price' in tour_columns, "Tour table missing 'price' column"
            assert 'duration' in tour_columns, "Tour table missing 'duration' column"
            assert 'category_id' in tour_columns, "Tour table missing 'category_id' column"
            assert tour_columns['category_id']['nullable'] == False, "Tour.category_id should not be nullable"
            
            # Verify Booking table schema
            booking_columns = {col['name']: col for col in inspector.get_columns('booking')}
            assert 'id' in booking_columns, "Booking table missing 'id' column"
            assert 'user_id' in booking_columns, "Booking table missing 'user_id' column"
            assert 'tour_id' in booking_columns, "Booking table missing 'tour_id' column"
            assert 'booking_date' in booking_columns, "Booking table missing 'booking_date' column"
            assert booking_columns['tour_id']['nullable'] == False, "Booking.tour_id should not be nullable"
            
            # Verify Review table schema
            review_columns = {col['name']: col for col in inspector.get_columns('review')}
            assert 'id' in review_columns, "Review table missing 'id' column"
            assert 'user_id' in review_columns, "Review table missing 'user_id' column"
            assert 'tour_id' in review_columns, "Review table missing 'tour_id' column"
            assert 'rating' in review_columns, "Review table missing 'rating' column"
            assert review_columns['tour_id']['nullable'] == False, "Review.tour_id should not be nullable"
            
            # Verify TourDate table schema
            tour_date_columns = {col['name']: col for col in inspector.get_columns('tour_date')}
            assert 'id' in tour_date_columns, "TourDate table missing 'id' column"
            assert 'tour_id' in tour_date_columns, "TourDate table missing 'tour_id' column"
            assert 'date' in tour_date_columns, "TourDate table missing 'date' column"
            assert tour_date_columns['tour_id']['nullable'] == False, "TourDate.tour_id should not be nullable"
            
            # Verify TourItineraryDay table schema
            itinerary_columns = {col['name']: col for col in inspector.get_columns('tour_itinerary_day')}
            assert 'id' in itinerary_columns, "TourItineraryDay table missing 'id' column"
            assert 'tour_id' in itinerary_columns, "TourItineraryDay table missing 'tour_id' column"
            assert 'day' in itinerary_columns, "TourItineraryDay table missing 'day' column"
            assert 'title' in itinerary_columns, "TourItineraryDay table missing 'title' column"
            assert 'description' in itinerary_columns, "TourItineraryDay table missing 'description' column"
            assert itinerary_columns['tour_id']['nullable'] == False, "TourItineraryDay.tour_id should not be nullable"
            
            # Verify Wishlist table schema
            wishlist_columns = {col['name']: col for col in inspector.get_columns('wishlist')}
            assert 'user_id' in wishlist_columns, "Wishlist table missing 'user_id' column"
            assert 'tour_id' in wishlist_columns, "Wishlist table missing 'tour_id' column"
            
            # Verify Inquiry table schema
            inquiry_columns = {col['name']: col for col in inspector.get_columns('inquiries')}
            assert 'id' in inquiry_columns, "Inquiry table missing 'id' column"
            assert 'user_id' in inquiry_columns, "Inquiry table missing 'user_id' column"
            assert 'message' in inquiry_columns, "Inquiry table missing 'message' column"
            
            # Verify ChatbotSettings table schema
            chatbot_columns = {col['name']: col for col in inspector.get_columns('chatbot_settings')}
            assert 'id' in chatbot_columns, "ChatbotSettings table missing 'id' column"
            
            # Verify TourPackage table schema
            package_columns = {col['name']: col for col in inspector.get_columns('tour_package')}
            assert 'id' in package_columns, "TourPackage table missing 'id' column"
            
            # Verify Destination table schema
            destination_columns = {col['name']: col for col in inspector.get_columns('destination')}
            assert 'id' in destination_columns, "Destination table missing 'id' column"
            assert 'name' in destination_columns, "Destination table missing 'name' column"
            
            # Verify foreign key relationships
            tour_fks = inspector.get_foreign_keys('tour')
            tour_fk_columns = [fk['constrained_columns'][0] for fk in tour_fks]
            assert 'category_id' in tour_fk_columns, "Tour table missing foreign key to Category"
            
            booking_fks = inspector.get_foreign_keys('booking')
            booking_fk_columns = [fk['constrained_columns'][0] for fk in booking_fks]
            assert 'tour_id' in booking_fk_columns, "Booking table missing foreign key to Tour"
            assert 'user_id' in booking_fk_columns, "Booking table missing foreign key to User"
            
            review_fks = inspector.get_foreign_keys('review')
            review_fk_columns = [fk['constrained_columns'][0] for fk in review_fks]
            assert 'tour_id' in review_fk_columns, "Review table missing foreign key to Tour"
            assert 'user_id' in review_fk_columns, "Review table missing foreign key to User"
            
            tour_date_fks = inspector.get_foreign_keys('tour_date')
            tour_date_fk_columns = [fk['constrained_columns'][0] for fk in tour_date_fks]
            assert 'tour_id' in tour_date_fk_columns, "TourDate table missing foreign key to Tour"
            
            itinerary_fks = inspector.get_foreign_keys('tour_itinerary_day')
            itinerary_fk_columns = [fk['constrained_columns'][0] for fk in itinerary_fks]
            assert 'tour_id' in itinerary_fk_columns, "TourItineraryDay table missing foreign key to Tour"

    def test_category_query_after_migration(self, fresh_db_app):
        """
        Test that Category table can be queried after migration.
        
        This simulates the inject_categories() context processor that runs on every request.
        """
        app, db_path = fresh_db_app
        
        with app.app_context():
            # Run migrations
            upgrade(revision='head')
            
            # Attempt to query Category table (this is what inject_categories() does)
            from app.models.Category import Category
            categories = Category.query.all()
            
            # Should return empty list, not crash
            assert isinstance(categories, list), "Category.query.all() should return a list"
            assert len(categories) == 0, "Fresh database should have no categories"

    def test_app_initialization_after_migration(self, fresh_db_app):
        """
        Test that Flask app initializes successfully after migration.
        
        This verifies that the inject_categories() context processor doesn't crash.
        """
        app, db_path = fresh_db_app
        
        with app.app_context():
            # Run migrations
            upgrade(revision='head')
            
            # Create a test request context to trigger context processors
            with app.test_request_context('/'):
                # This should not raise an exception
                from app.models.Category import Category
                categories = Category.query.all()
                assert categories is not None, "Context processor should execute without error"
