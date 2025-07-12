from app import db
from datetime import datetime
import uuid

class Booking(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)
    # Remove default here since you're setting it manually in the code
    reference = db.Column(db.String(36), unique=True, nullable=False)

    user_id = db.Column(db.Integer, nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)

    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    num_people = db.Column(db.Integer, default=1, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)

    # These should not be nullable since your form requires them
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)

    # Payment related fields - payment_method and payment_status should not be nullable
    payment_method = db.Column(db.String(20), nullable=False)
    payment_status = db.Column(db.String(20), nullable=False, default='pending')
    payment_reference = db.Column(db.String(100), nullable=True)
    payment_details = db.Column(db.String(255), nullable=True)


 #✅ New field for Pesapal tracking
    order_tracking_id = db.Column(db.String(100), nullable=True)
    # Cancellation tracking fields
    cancellation_reason = db.Column(db.String(50), nullable=True)
    cancellation_notes = db.Column(db.Text, nullable=True)
    cancelled_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    package = db.relationship('Package', back_populates='bookings')

    def cancel(self, reason=None, notes=None):
        """Mark booking as cancelled with optional reason and notes."""
        self.cancellation_reason = reason
        self.cancellation_notes = notes
        self.cancelled_at = datetime.utcnow()
        self.payment_status = 'cancelled'  # Update payment status too
        return self

    def __repr__(self):
        return f'<Booking {self.reference}>'