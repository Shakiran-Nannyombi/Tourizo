from flask import Flask, render_template
from flask_migrate import Migrate

# Blueprint imports (to be implemented in respective files)
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Import and register blueprints (stubs for now)
    from .auth import auth_bp
    from .tours import tours_bp
    from .bookings import bookings_bp
    from .admin import admin_bp
    from .reviews import reviews_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tours_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reviews_bp)

    @app.route('/')
    def welcome():
        return render_template('welcome.html')

    # Context processors
    @app.context_processor
    def inject_categories():
        from app.models.Category import Category
        return dict(categories=Category.query.all())

    @app.context_processor
    def inject_moment():
        from app.extensions import moment
        return dict(moment=moment)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        from app.extensions import db
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template('errors/401.html'), 401

    # Initialize Flask-Migrate
    from app.extensions import db
    db.init_app(app)
    migrate = Migrate(app, db)

    from app.extensions import login_manager
    login_manager.init_app(app)

    from app.models.User import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
