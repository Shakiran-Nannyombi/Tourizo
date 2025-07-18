from datetime import datetime
from app.extensions import db

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
