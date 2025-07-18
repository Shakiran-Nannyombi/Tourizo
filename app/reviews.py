from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.Review import Review
from app.models.Tour import Tour
from app.forms import ReviewForm
from app.extensions import db

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

def register_routes():
    @reviews_bp.route('/add/<int:tour_id>', methods=['GET', 'POST'])
    def add_review(tour_id):
        tour = Tour.query.get_or_404(tour_id)
        form = ReviewForm()
        if form.validate_on_submit():
            review = Review(
                rating=form.rating.data,
                comment=form.comment.data,
                reviewer_name=form.reviewer_name.data,
                reviewer_email=form.reviewer_email.data,
                tour_id=tour_id,
                user_id=None  # Set user_id if user is logged in
            )
            db.session.add(review)
            db.session.commit()
            flash('Review submitted! It will be visible once approved.', 'success')
            return redirect(url_for('tours.tour_detail', tour_id=tour_id))
        return render_template('reviews/add_review.html', form=form, tour=tour)

register_routes()
