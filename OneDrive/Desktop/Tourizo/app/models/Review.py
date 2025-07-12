from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tour_id = db.Column(db.Integer, db.ForeignKey('tour_package.id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    # Add more fields as needed
