from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tour_id = db.Column(db.Integer, db.ForeignKey('tour_package.id'))
    status = db.Column(db.String(20), default='pending')
    # Add more fields as needed
