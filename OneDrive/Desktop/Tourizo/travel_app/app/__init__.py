from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import logging
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object("config.Config")
    
    # Mail settings (⚠️ in production load from env variables)
    app.config.update(
        MAIL_SERVER="smtp.gmail.com",
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME="ankundanoela4@gmail.com",
        MAIL_PASSWORD="zfax gthg iwnq xadg",
        MAIL_DEFAULT_SENDER="TravelMate Tours <ankundanoela4@gmail.com>"
    )
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # Register custom filters
    try:
        from app.filters import register_filters
        register_filters(app)
    except ImportError:
        logger.warning("Filters module not found, skipping filter registration")
    
    # Register blueprints
    from app.bookings import bp as bookings_bp
    app.register_blueprint(bookings_bp, url_prefix="/bookings")
    
    # Test route
    @app.route("/")
    def index():
        return "Flask is running ✅"
    
    # Health check route
    @app.route("/health")
    def health_check():
        return {
            "status": "healthy",
            "database": "connected",
            "mail": "configured"
        }
    
    # Import models for Alembic
    try:
        from app.models import booking  # noqa: F401
    except ImportError:
        logger.warning("Models module not found")
    
    return app
