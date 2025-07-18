from app.extensions import db

class TourDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)
    price_override = db.Column(db.Float)
    is_available = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<TourDate {self.date} for Tour {self.tour_id}>' 