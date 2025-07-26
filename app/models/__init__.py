# app/__init__.py
from flask import Flask
from app.extensions import db  # ✅ Use shared db instance

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # Register blueprints here
    from app.admin import admin_bp
    from app.auth import auth_bp
    from app.contact import contact_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(contact_bp)

    return app
