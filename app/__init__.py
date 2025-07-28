from flask import Flask, render_template
from flask_migrate import Migrate

# External blueprint imports (at top level)
from app.auth import auth_bp
from app.tours import tours_bp
from app.bookings import bookings_bp
from app.admin import admin_bp
from app.reviews import reviews_bp
from app.contact import contact_bp  # Contact blueprint
from app.policies import policies_bp  # Policies blueprint

# Extension imports
from app.extensions import db, login_manager, mail, moment

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    Migrate(app, db)

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
        from app.models.Category import Category
        return dict(categories=Category.query.all())

    @app.context_processor
    def inject_moment():
        return dict(moment=moment)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

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

    return app
