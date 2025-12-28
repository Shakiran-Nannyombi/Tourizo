import pytest

def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    # Add a check for some content on the page
    assert b'Tourizo' in response.data or b'Welcome' in response.data

def test_login_page_load(client):
    """Test that the login page loads."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_database_connectivity(app):
    """Test that the database is initialized and accessible."""
    from app import db
    with app.app_context():
        # Check if we can execute a simple query
        assert db.engine.connect() is not None
