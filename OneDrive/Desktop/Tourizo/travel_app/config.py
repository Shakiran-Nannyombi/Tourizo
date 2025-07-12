import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    # Core Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Database
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/travel_app"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email settings
    MAIL_SERVER = "localhost"
    MAIL_PORT = 8025
    MAIL_DEFAULT_SENDER = "noreply@travel.test"

    # Pesapal credentials
    PESAPAL_CONSUMER_KEY = os.getenv("PESAPAL_CONSUMER_KEY")
    PESAPAL_CONSUMER_SECRET = os.getenv("PESAPAL_CONSUMER_SECRET")
    PESAPAL_IPN_URL = 'https://your-actual-domain.com/payment/callback'
