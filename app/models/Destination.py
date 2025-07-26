from app.extensions import db

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    country = db.Column(db.String(100), nullable=False) 