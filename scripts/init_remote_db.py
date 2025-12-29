
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
# Import all models to ensure they are registered with SQLAlchemy
from app.models.User import User
from app.models.Tour import Tour, TourItineraryDay
from app.models.TourDate import TourDate
from app.models.Category import Category
from app.models.Booking import Booking
from app.models.Review import Review
from app.models.Inquiry import Inquiry
from app.models.ChatbotSettings import ChatbotSettings
from app.models.Destination import Destination
from app.models.TourPackage import TourPackage

app = create_app()

with app.app_context():
    print("Creating all tables in the database...")
    try:
        db.create_all()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
