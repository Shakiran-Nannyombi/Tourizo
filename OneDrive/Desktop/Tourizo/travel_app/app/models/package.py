from app import db

class Package(db.Model):
    __tablename__ = "package"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price_per_person = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)

    bookings = db.relationship('Booking', back_populates='package')
