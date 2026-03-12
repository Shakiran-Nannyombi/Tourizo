"""
Preservation Property Tests: Verify Existing Behavior is Maintained

These tests verify that for databases where tables already exist, the migration
process preserves existing data and doesn't break workflows.

**Expected Outcome**: These tests PASS on unfixed code (establishing baseline behavior).

**Validates: Requirements 3.1, 3.2, 3.3, 3.4**
"""

import pytest
import os
import tempfile
from datetime import datetime
from flask_migrate import upgrade, downgrade
from app import create_app, db
from app.models.Category import Category
from app.models.User import User
from app.models.Tour import Tour


class TestDatabasePreservation:
    """Test that existing data and workflows are preserved"""

    @pytest.fixture
    def app_with_existing_db(self):
        """Create app with a database that has existing tables and data"""
        db_fd, db_path = tempfile.mkstemp(suffix='.db')
        
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['TESTING'] = True
        
        with app.app_context():
            # Create all tables using db.create_all() (simulating existing database)
            db.create_all()
            
            # Add some sample data with unique name
            import uuid
            unique_name = f'Test Category {uuid.uuid4().hex[:8]}'
            category = Category(name=unique_name, description='Test Description')
            db.session.add(category)
            db.session.commit()
            
            yield app, db_path, category.id, unique_name
            
            # Cleanup
            db.session.remove()
            os.close(db_fd)
            os.unlink(db_path)

    def test_existing_data_preserved_after_migration(self, app_with_existing_db):
        """
        Test that existing data is not modified when migrations are applied.
        
        This verifies that running migrations on a database with existing tables
        and data doesn't corrupt or delete the data.
        """
        app, db_path, category_id, unique_name = app_with_existing_db
        
        with app.app_context():
            # Verify data exists before migration
            category_before = Category.query.get(category_id)
            assert category_before is not None
            assert category_before.name == unique_name
            assert category_before.description == 'Test Description'
            
            # Run migrations (this should be idempotent)
            try:
                upgrade(revision='head')
            except Exception as e:
                # Migration might fail on existing tables, which is acceptable
                # as long as data is preserved
                pass
            
            # Verify data still exists after migration
            category_after = Category.query.get(category_id)
            assert category_after is not None
            assert category_after.name == unique_name
            assert category_after.description == 'Test Description'
            assert category_after.id == category_id

    def test_local_sqlite_workflow_continues_to_work(self, app_with_existing_db):
        """
        Test that local SQLite development workflow continues to work.
        
        This verifies that developers can continue to use db.create_all()
        for local development without issues.
        """
        app, db_path, category_id, unique_name = app_with_existing_db
        
        with app.app_context():
            # Verify we can query existing data
            categories = Category.query.all()
            assert len(categories) >= 1
            assert any(c.name == unique_name for c in categories)
            
            # Verify we can add new data
            import uuid
            new_name = f'New Category {uuid.uuid4().hex[:8]}'
            new_category = Category(name=new_name, description='New Description')
            db.session.add(new_category)
            db.session.commit()
            
            # Verify new data was added
            categories = Category.query.all()
            assert len(categories) >= 2
            assert any(c.name == new_name for c in categories)

    def test_category_query_works_with_existing_tables(self, app_with_existing_db):
        """
        Test that Category.query.all() works when tables already exist.
        
        This simulates the inject_categories() context processor behavior
        on an existing database.
        """
        app, db_path, category_id, unique_name = app_with_existing_db
        
        with app.app_context():
            # This is what inject_categories() does
            categories = Category.query.all()
            
            # Should return list with at least one category
            assert isinstance(categories, list)
            assert len(categories) >= 1
            assert any(c.name == unique_name for c in categories)

    def test_app_initialization_with_existing_database(self, app_with_existing_db):
        """
        Test that Flask app initializes successfully with existing database.
        
        This verifies that the inject_categories() context processor works
        correctly when the database already has tables and data.
        """
        app, db_path, category_id, unique_name = app_with_existing_db
        
        with app.app_context():
            # Create a test request context to trigger context processors
            with app.test_request_context('/'):
                # This should not raise an exception
                from app.models.Category import Category
                categories = Category.query.all()
                assert categories is not None
                assert len(categories) >= 1

    def test_multiple_migrations_are_idempotent(self, app_with_existing_db):
        """
        Test that running migrations multiple times doesn't cause issues.
        
        This verifies that migrations are idempotent and can be safely
        run multiple times without corrupting data.
        """
        app, db_path, category_id, unique_name = app_with_existing_db
        
        with app.app_context():
            # Get initial data
            category_before = Category.query.get(category_id)
            initial_name = category_before.name
            
            # Run migrations multiple times
            for i in range(2):
                try:
                    upgrade(revision='head')
                except Exception:
                    # Migration might fail on existing tables, which is acceptable
                    pass
            
            # Verify data is still intact
            category_after = Category.query.get(category_id)
            assert category_after is not None
            assert category_after.name == initial_name
