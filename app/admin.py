from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.Review import Review   # ✅ CORRECT
from flask_login import login_required
from app.models.Tour import Tour
from app.models.Category import Category
from sqlalchemy import func, extract
from app.forms import TourForm
from app.extensions import db
import logging
from app.models.Inquiry import Inquiry
from functools import wraps
from flask import make_response
import datetime
from app.models.Booking import Booking 

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

logging.basicConfig(filename='admin.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Decorator to prevent caching of protected pages
def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return no_cache

@admin_bp.route('/dashboard')
@login_required
@nocache
def dashboard():
    from sqlalchemy import func
    total_tours = Tour.query.count()
    active_tours = Tour.query.filter_by(is_active=True).count()
    featured_tours = Tour.query.filter_by(is_featured=True).count()
    draft_tours = Tour.query.filter_by(is_active=False).count()
    recent_tours = Tour.query.order_by(Tour.created_at.desc()).limit(5).all()
    current_time = datetime.datetime.utcnow()
    category_count = Category.query.count()
    return render_template(
        'admin/dashboard.html',
        tour_count=total_tours,
        category_count=category_count,
        total_tours=total_tours,
        active_tours=active_tours,
        featured_tours=featured_tours,
        draft_tours=draft_tours,
        recent_tours=recent_tours,
        current_time=current_time
    )

@admin_bp.route('/tours')
@login_required
@nocache
def manage_tours():
    tours = Tour.query.all()
    return render_template('admin/manage_tours.html', tours=tours)

@admin_bp.route('/add-tour', methods=['GET', 'POST'])
@login_required
def add_tour():
    form = TourForm()
    if form.validate_on_submit():
        tour = Tour(
            title=form.title.data,
            description=form.description.data,
            short_description=form.short_description.data,
            price=form.price.data,
            duration=form.duration.data,
            duration_type=form.duration_type.data,
            max_participants=form.max_participants.data,
            min_participants=form.min_participants.data,
            difficulty_level=form.difficulty_level.data,
            departure_location=form.departure_location.data,
            image=form.featured_image.data.filename if form.featured_image.data else None,
            image_gallery=None,  # Handle gallery upload as needed
            inclusions=form.inclusions.data,
            exclusions=form.exclusions.data,
            itinerary=form.itinerary.data,
            available_from=form.available_from.data,
            available_to=form.available_to.data,
            is_active=form.is_active.data,
            is_featured=form.is_featured.data,
            meta_title=form.meta_title.data,
            meta_description=form.meta_description.data,
            category_id=form.category_id.data,
            destination=form.destination.data
        )
        db.session.add(tour)
        db.session.commit()
        flash('Tour added successfully!', 'success')
        return redirect(url_for('admin.manage_tours'))
    return render_template('admin/add_tour.html', form=form)

@admin_bp.route('/edit-tour/<int:tour_id>', methods=['GET', 'POST'])
@login_required
def edit_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    form = TourForm(obj=tour)
    if form.validate_on_submit():
        form.populate_obj(tour)
        db.session.commit()
        flash('Tour updated successfully!', 'success')
        return redirect(url_for('admin.manage_tours'))
    return render_template('admin/edit_tour.html', form=form, tour=tour)

@admin_bp.route('/tour-detail/<int:tour_id>')
@login_required
def tour_detail(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    return render_template('admin/tour_detail.html', tour=tour)

@admin_bp.route('/inquiries')
@login_required
def inquiries():
    all_inquiries = Inquiry.query.order_by(Inquiry.timestamp.desc()).all()
    return render_template('admin/manage_inquiries.html', inquiries=all_inquiries)

@admin_bp.route('/inquiry/<int:inquiry_id>')
@login_required
def inquiry_detail(inquiry_id):
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    return render_template('admin/inquiry_detail.html', inquiry=inquiry)

@admin_bp.route('/inquiry/<int:inquiry_id>/delete', methods=['POST', 'GET'])
@login_required
def inquiry_delete(inquiry_id):
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    db.session.delete(inquiry)
    db.session.commit()
    flash('Inquiry deleted successfully!', 'success')
    return redirect(url_for('admin.inquiries'))

@admin_bp.route('/users')
@login_required
def manage_users():
    from app.models.User import User  # <- Case-sensitive
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not (name and email and message):
            flash('All fields are required!', 'danger')
            return redirect(url_for('admin.contact'))

        new_inquiry = Inquiry(name=name, email=email, message=message)
        db.session.add(new_inquiry)
        db.session.commit()

        logging.info(f'New inquiry from {email}')
        flash('Thank you for your inquiry!', 'success')
        return redirect(url_for('admin.contact'))

    return render_template('contact_form.html')

# Reports routes
@admin_bp.route('/reports/booking-report')
@login_required
def booking_report():
    bookings_by_month = (
        db.session.query(
            extract('year', Booking.booking_date).label('year'),
            extract('month', Booking.booking_date).label('month'),
            func.count(Booking.id).label('total_bookings')
        )
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )

    return render_template(
        'admin/reports/bookings.html',
        bookings_by_month=bookings_by_month,
        now=datetime.datetime.utcnow()
    )

@admin_bp.route('/reports/revenue-report')
@login_required
def revenue_report():
    revenue_by_month = (
        db.session.query(
            extract('year', Booking.booking_date).label('year'),
            extract('month', Booking.booking_date).label('month'),
            func.sum(Booking.total_amount).label('total_revenue')  
        )
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )

    return render_template(
        'admin/reports/revenue.html',
        revenue_by_month=revenue_by_month,
        now=datetime.datetime.utcnow()
    )

@admin_bp.route('/users/<int:user_id>')
@login_required
def admin_user_detail(user_id):
    from app.models.User import User
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_detail.html', user=user)



@admin_bp.route('/reports/popular-destinations')
@login_required
def popular_destinations():
    # Query to get popular destinations based on booking counts
    popular_destinations = (
        db.session.query(
            Tour.destination,
            Tour.title,
            func.count(Booking.id).label('booking_count')
        )
        .join(Booking, Tour.id == Booking.tour_id)
        .group_by(Tour.destination, Tour.title)
        .order_by(func.count(Booking.id).desc())
        .limit(10)  # Top 10 popular destinations
        .all()
    )
    
    return render_template(
        'admin/reports/popular_destinations.html', 
        popular_destinations=popular_destinations
    )
@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    # Your logic here
    return render_template('admin/edit_user.html', user_id=user_id)

@admin_bp.route('/reviews/<int:review_id>/approve')
@login_required
def approve_review(review_id):
    review = Review.query.get_or_404(review_id)
    review.is_approved = True
    db.session.commit()
    flash('Review approved.', 'success')
    return redirect(url_for('admin.review_list'))

@admin_bp.route('/reviews')
@login_required
# @admin_required  # Optional: restrict to admins only
def admin_reviews():
    reviews = Review.query.order_by(Review.id.desc()).all()
    return render_template('admin/manage_reviews.html', reviews=reviews)