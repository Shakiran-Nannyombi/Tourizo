from flask import Flask, render_template
from flask_login import AnonymousUserMixin
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

# External blueprint imports (at top level)
from app.auth import auth_bp
from app.tours import tours_bp
from app.bookings import bookings_bp
from app.admin import admin_bp
from app.reviews import reviews_bp
from app.contact import contact_bp  # Contact blueprint
from app.policies import policies_bp  # Policies blueprint
from app.api.chatbot import chatbot_bp
from app.bootstrap import prepare_database, resolve_database_uri

# Extension imports
from app.extensions import db, login_manager, mail, moment


class GuestUser(AnonymousUserMixin):
    """Public pages read username even when nobody is logged in."""

    username = "Guest"
    is_admin = False

    @property
    def wishlist(self):
        return []


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = resolve_database_uri(
        app.config.get('SQLALCHEMY_DATABASE_URI')
    )

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    Migrate(app, db)
    login_manager.anonymous_user = GuestUser

    # Set login view for unauthorized users to redirect to welcome page
    login_manager.login_view = 'welcome'  # Redirect unauthorized users here

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tours_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(policies_bp)
    app.register_blueprint(chatbot_bp)

    # Home route - welcome page
    @app.route('/')
    def welcome():
        return render_template('welcome.html')

    # About route
    @app.route('/about')
    def about():
        return render_template('about.html')

    # Video gallery route
    @app.route('/video-gallery')
    def video_gallery():
        return render_template('video_gallery.html')

    # Context processors
    @app.context_processor
    def inject_categories():
        try:
            from app.models.Category import Category
            return dict(categories=Category.query.all())
        except Exception:
            app.logger.exception("Could not load categories for the template")
            db.session.rollback()
            return dict(categories=[])

    @app.context_processor
    def inject_moment():
        return dict(moment=moment)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(Exception)
    def internal_error(error):
        if isinstance(error, HTTPException):
            return error
        app.logger.exception("Unhandled exception")
        db.session.rollback()
        try:
            return render_template('errors/500.html'), 500
        except Exception:
            app.logger.exception("Error page failed to render")
            return "Internal Server Error", 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template('errors/401.html'), 401

    # User loader for Flask-Login
    from app.models.User import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Custom Jinja filters
    from app.utils import from_json
    app.jinja_env.filters['from_json'] = from_json

    prepare_database(app)
    return app
