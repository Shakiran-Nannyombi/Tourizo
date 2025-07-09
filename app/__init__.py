from flask import Flask

# Blueprint imports (to be implemented in respective files)
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

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

    return app
