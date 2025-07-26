from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.Tour import Tour     # <-- IMPORTANT: import the class, not the module
from app.models.Review import Review
from app.extensions import db
from app.forms import ReviewForm

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@reviews_bp.route('/add/<int:tour_id>', methods=['GET', 'POST'])
@login_required
def add_review(tour_id):
    # This works ONLY if Tour is the model class, imported properly
    tour = Tour.query.get_or_404(tour_id)  
    
    form = ReviewForm()

    if request.method == 'GET':
        form.reviewer_name.data = current_user.username
        form.reviewer_email.data = current_user.email

    if form.validate_on_submit():
        review = Review(
            rating=form.rating.data,
            reviewer_name=form.reviewer_name.data,
            reviewer_email=form.reviewer_email.data,
            comment=form.comment.data,
            tour_id=tour.id,
            user_id=current_user.id,
            is_verified=True,
            is_approved=True
        )
        db.session.add(review)
        db.session.commit()
        flash("Thank you for your review!", "success")
        return redirect(url_for('tours.tour_detail', tour_id=tour.id))

    return render_template('reviews/add_review.html', form=form, tour=tour)
