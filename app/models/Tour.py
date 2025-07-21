from datetime import datetime
from app.extensions import db

class TourItineraryDay(db.Model):
    __tablename__ = 'tour_itinerary_day'
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

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
    itinerary_days = db.relationship('TourItineraryDay', backref='tour', order_by='TourItineraryDay.day', cascade='all, delete-orphan')

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

    @property
    def featured_image(self):
        if self.image:
            return f'images/tours/{self.image}'
        return None
 