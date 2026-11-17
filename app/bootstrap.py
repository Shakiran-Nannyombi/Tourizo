"""Prepare a usable database before the first request.

The SQLite file committed for Render is stamped at the Alembic head but has
no application tables. Migrations only alter existing tables, so `flask db
upgrade` never creates them. Every template also loads categories, and the
error page does the same, so a missing table becomes a generic 500.
"""

import logging
import os

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def default_sqlite_uri():
    instance_dir = os.path.join(PROJECT_ROOT, "instance")
    os.makedirs(instance_dir, exist_ok=True)
    return "sqlite:///" + os.path.join(instance_dir, "travel_app.db")


def ensure_sqlite_directory(uri):
    if not uri.startswith("sqlite:///") or ":memory:" in uri:
        return
    path = uri[len("sqlite:///"):]
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def resolve_database_uri(configured_uri):
    """Return a database URL that can actually be opened.

    A leftover DATABASE_URL (the old Supabase setting on Render) is ignored
    when that server does not answer, so the site can still boot on SQLite.
    """
    uri = configured_uri or default_sqlite_uri()
    if uri.startswith("sqlite"):
        if uri in ("sqlite://", "sqlite:", "sqlite:///"):
            uri = default_sqlite_uri()
        ensure_sqlite_directory(uri)
        return uri

    connect_args = {"connect_timeout": 5} if uri.startswith("postgres") else {}
    try:
        engine = create_engine(uri, pool_pre_ping=True, connect_args=connect_args)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        engine.dispose()
        return uri
    except Exception as exc:
        logger.error(
            "DATABASE_URL is unreachable (%s). Using local SQLite instead.", exc
        )
        return default_sqlite_uri()


def prepare_database(app):
    from app.extensions import db
    from app.models.Booking import Booking  # noqa: F401
    from app.models.Category import Category  # noqa: F401
    from app.models.ChatbotSettings import ChatbotSettings  # noqa: F401
    from app.models.Destination import Destination  # noqa: F401
    from app.models.Inquiry import Inquiry  # noqa: F401
    from app.models.Review import Review  # noqa: F401
    from app.models.Tour import Tour, TourItineraryDay  # noqa: F401
    from app.models.TourDate import TourDate  # noqa: F401
    from app.models.User import User  # noqa: F401

    with app.app_context():
        try:
            db.create_all()
            _seed_if_empty(app)
        except SQLAlchemyError:
            db.session.rollback()
            app.logger.exception("Could not prepare the database")


def _seed_if_empty(app):
    from werkzeug.security import generate_password_hash

    from app.extensions import db
    from app.models.Category import Category
    from app.models.Tour import Tour
    from app.models.User import User

    if Category.query.count() == 0 or Tour.query.count() == 0:
        from scripts.seed_tours import (
            create_categories,
            create_sample_itineraries,
            create_sample_tours,
        )

        categories = create_categories()
        if Tour.query.count() == 0:
            create_sample_tours(categories)
            create_sample_itineraries(Tour.query.all())
        app.logger.info("Seeded demo categories and tours")

    if User.query.filter_by(is_admin=True).first() is None:
        db.session.add(
            User(
                username="admin",
                email="devkiran256@gmail.com",
                password_hash=generate_password_hash("admin123"),
                is_admin=True,
            )
        )
        db.session.commit()
        app.logger.info("Created default admin user")
