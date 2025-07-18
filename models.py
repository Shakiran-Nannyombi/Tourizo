from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    country = db.Column(db.String(100), nullable=False)


class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(300))
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    duration_type = db.Column(db.String(20), default='Days')
    max_participants = db.Column(db.Integer, default=20)
    min_participants = db.Column(db.Integer, default=1)
    difficulty_level = db.Column(db.String(20), default='Easy')

    departure_location = db.Column(db.String(200))
    image = db.Column(db.String(200))
    image_gallery = db.Column(db.Text)

    inclusions = db.Column(db.Text)
    exclusions = db.Column(db.Text)
    itinerary = db.Column(db.Text)

    available_from = db.Column(db.Date)
    available_to = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)

    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(300))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='tours')

    destination = db.Column(db.String(100), nullable=False)

    bookings = db.relationship('Booking', backref='tour', lazy=True)
    reviews = db.relationship('Review', backref='tour', lazy=True)
    available_dates = db.relationship('TourDate', backref='tour', lazy=True)

    def __repr__(self):
        return f'<Tour {self.title}>'

    @property
    def average_rating(self):
        if self.reviews:
            return sum(review.rating for review in self.reviews) / len(self.reviews)
        return 0

    @property
    def total_bookings(self):
        return len(self.bookings)

    @property
    def is_available(self):
        if not self.is_active:
            return False
        today = datetime.utcnow().date()
        if self.available_from and self.available_to:
            return self.available_from <= today <= self.available_to
        return True


class Booking(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(36), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)

    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)

    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=True)
    num_people = db.Column(db.Integer, nullable=False, default=1)
    special_requests = db.Column(db.Text)

    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(20), nullable=True)
    payment_status = db.Column(db.String(20), nullable=False, default='pending')
    payment_reference = db.Column(db.String(100))
    payment_details = db.Column(db.String(255))
    order_tracking_id = db.Column(db.String(100))

    cancellation_reason = db.Column(db.String(50))
    cancellation_notes = db.Column(db.Text)
    cancelled_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def cancel(self, reason=None, notes=None):
        self.cancellation_reason = reason
        self.cancellation_notes = notes
        self.cancelled_at = datetime.utcnow()
        self.payment_status = 'cancelled'
        return self

    def __repr__(self):
        return f'<Booking {self.reference}>'


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    reviewer_name = db.Column(db.String(100), nullable=False)
    reviewer_email = db.Column(db.String(120))
    is_verified = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class TourDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)
    price_override = db.Column(db.Float)
    is_available = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<TourDate {self.date} for Tour {self.tour_id}>'
