from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
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
from app.models import ChatbotSettings, db
from flask import abort
from flask_login import login_required, current_user
import csv
import io
import json
from app.forms import EditUserForm
from app.models.User import User

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

@admin_bp.route('/invite-user', methods=['GET', 'POST'])
@login_required
def invite_user():
    # You can add POST handling here if you want to process the form
    return render_template('admin/invite_user.html')

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

    return render_template('contact.html')

# Reports routes
@admin_bp.route('/reports/booking-report')
@login_required
def booking_report():
    # Get date range filter from query parameters
    months_filter = request.args.get('months', '12')
    try:
        months_filter = int(months_filter)
    except (ValueError, TypeError):
        months_filter = 12
    
    # Calculate the date range
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=30 * months_filter)
    
    bookings_by_month = (
        db.session.query(
            extract('year', Booking.booking_date).label('year'),
            extract('month', Booking.booking_date).label('month'),
            func.count(Booking.id).label('total_bookings')
        )
        .filter(Booking.booking_date >= start_date)
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )

    return render_template(
        'admin/reports/bookings.html',
        bookings_by_month=bookings_by_month,
        now=datetime.datetime.utcnow(),
        months_filter=months_filter
    )

@admin_bp.route('/reports/revenue-report')
@login_required
def revenue_report():
    # Get date range filter from query parameters
    months_filter = request.args.get('months', '12')
    try:
        months_filter = int(months_filter)
    except (ValueError, TypeError):
        months_filter = 12
    
    # Calculate the date range
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=30 * months_filter)
    
    revenue_by_month = (
        db.session.query(
            extract('year', Booking.booking_date).label('year'),
            extract('month', Booking.booking_date).label('month'),
            func.sum(Booking.total_amount).label('total_revenue')  
        )
        .filter(Booking.booking_date >= start_date)
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )

    # Convert Decimal values to float for template rendering
    revenue_by_month_processed = []
    for row in revenue_by_month:
        revenue_by_month_processed.append({
            'year': row.year,
            'month': row.month,
            'total_revenue': float(row.total_revenue or 0)
        })
    
    return render_template(
        'admin/reports/revenue.html',
        revenue_by_month=revenue_by_month_processed,
        now=datetime.datetime.utcnow(),
        months_filter=months_filter
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
    # Get date range filter from query parameters
    months_filter = request.args.get('months', '12')
    try:
        months_filter = int(months_filter)
    except (ValueError, TypeError):
        months_filter = 12
    
    # Calculate the date range
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=30 * months_filter)
    
    # Query to get popular destinations based on booking counts
    popular_destinations = (
        db.session.query(
            Tour.destination,
            Tour.title,
            func.count(Booking.id).label('booking_count')
        )
        .join(Booking, Tour.id == Booking.tour_id)
        .filter(Booking.booking_date >= start_date)
        .group_by(Tour.destination, Tour.title)
        .order_by(func.count(Booking.id).desc())
        .limit(10)  # Top 10 popular destinations
        .all()
    )
    
    return render_template(
        'admin/reports/popular_destinations.html', 
        popular_destinations=popular_destinations,
        now=datetime.datetime.utcnow(),
        months_filter=months_filter
    )

# Export Routes
@admin_bp.route('/reports/export/bookings')
@login_required
def export_bookings():
    # Get date range filter from query parameters
    months_filter = request.args.get('months', '12')
    try:
        months_filter = int(months_filter)
    except (ValueError, TypeError):
        months_filter = 12
    
    # Calculate the date range
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=30 * months_filter)
    
    bookings_by_month = (
        db.session.query(
            extract('year', Booking.booking_date).label('year'),
            extract('month', Booking.booking_date).label('month'),
            func.count(Booking.id).label('total_bookings')
        )
        .filter(Booking.booking_date >= start_date)
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )
    
    # Create CSV data
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Year', 'Month', 'Total Bookings'])
    
    for row in bookings_by_month:
        writer.writerow([row.year, row.month, row.total_bookings])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'bookings_report_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@admin_bp.route('/reports/export/revenue')
@login_required
def export_revenue():
    # Get date range filter from query parameters
    months_filter = request.args.get('months', '12')
    try:
        months_filter = int(months_filter)
    except (ValueError, TypeError):
        months_filter = 12
    
    # Calculate the date range
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=30 * months_filter)
    
    revenue_by_month = (
        db.session.query(
            extract('year', Booking.booking_date).label('year'),
            extract('month', Booking.booking_date).label('month'),
            func.sum(Booking.total_amount).label('total_revenue')
        )
        .filter(Booking.booking_date >= start_date)
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )
    
    # Create CSV data
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Year', 'Month', 'Total Revenue (USD)'])
    
    for row in revenue_by_month:
        writer.writerow([row.year, row.month, f"${float(row.total_revenue or 0):.2f}"])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'revenue_report_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@admin_bp.route('/reports/export/destinations')
@login_required
def export_destinations():
    # Get date range filter from query parameters
    months_filter = request.args.get('months', '12')
    try:
        months_filter = int(months_filter)
    except (ValueError, TypeError):
        months_filter = 12
    
    # Calculate the date range
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=30 * months_filter)
    
    popular_destinations = (
        db.session.query(
            Tour.destination,
            Tour.title,
            func.count(Booking.id).label('booking_count')
        )
        .join(Booking, Tour.id == Booking.tour_id)
        .filter(Booking.booking_date >= start_date)
        .group_by(Tour.destination, Tour.title)
        .order_by(func.count(Booking.id).desc())
        .all()
    )
    
    # Create CSV data
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Rank', 'Destination', 'Tour Title', 'Booking Count', 'Popularity %'])
    
    for i, dest in enumerate(popular_destinations, 1):
        total_bookings = sum(d.booking_count for d in popular_destinations)
        popularity = (dest.booking_count / total_bookings * 100) if total_bookings > 0 else 0
        writer.writerow([i, dest.destination, dest.title, dest.booking_count, f"{popularity:.1f}%"])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'destinations_report_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

# Analytics Routes
@admin_bp.route('/reports/analytics/bookings')
@login_required
def analytics_bookings():
    # Get date range filter from query parameters
    months_filter = request.args.get('months', '12')
    try:
        months_filter = int(months_filter)
    except (ValueError, TypeError):
        months_filter = 12
    
    # Calculate the date range
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=30 * months_filter)
    
    # Get booking data for charts
    bookings_by_month = (
        db.session.query(
            extract('year', Booking.booking_date).label('year'),
            extract('month', Booking.booking_date).label('month'),
            func.count(Booking.id).label('total_bookings')
        )
        .filter(Booking.booking_date >= start_date)
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )
    
    # Format data for charts
    chart_data = {
        'labels': [f"{row.month}/{row.year}" for row in bookings_by_month],
        'data': [row.total_bookings for row in bookings_by_month],
        'total_bookings': sum(row.total_bookings for row in bookings_by_month),
        'avg_bookings': sum(row.total_bookings for row in bookings_by_month) / len(bookings_by_month) if bookings_by_month else 0
    }
    
    return render_template(
        'admin/reports/analytics_bookings.html',
        chart_data=chart_data,
        bookings_by_month=bookings_by_month,
        now=datetime.datetime.utcnow(),
        months_filter=months_filter
    )

@admin_bp.route('/reports/analytics/revenue')
@login_required
def analytics_revenue():
    # Get date range filter from query parameters
    months_filter = request.args.get('months', '12')
    try:
        months_filter = int(months_filter)
    except (ValueError, TypeError):
        months_filter = 12
    
    # Calculate the date range
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=30 * months_filter)
    
    # Get revenue data for charts
    revenue_by_month = (
        db.session.query(
            extract('year', Booking.booking_date).label('year'),
            extract('month', Booking.booking_date).label('month'),
            func.sum(Booking.total_amount).label('total_revenue')
        )
        .filter(Booking.booking_date >= start_date)
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )
    
    # Format data for charts
    chart_data = {
        'labels': [f"{row.month}/{row.year}" for row in revenue_by_month],
        'data': [float(row.total_revenue or 0) for row in revenue_by_month],
        'total_revenue': float(sum(float(row.total_revenue or 0) for row in revenue_by_month)),
        'avg_revenue': float(sum(float(row.total_revenue or 0) for row in revenue_by_month) / len(revenue_by_month)) if revenue_by_month else 0.0
    }
    
    # Convert Decimal values to float for template rendering
    revenue_by_month_processed = []
    for row in revenue_by_month:
        revenue_by_month_processed.append({
            'year': row.year,
            'month': row.month,
            'total_revenue': float(row.total_revenue or 0)
        })
    
    return render_template(
        'admin/reports/analytics_revenue.html',
        chart_data=chart_data,
        revenue_by_month=revenue_by_month_processed,
        now=datetime.datetime.utcnow(),
        months_filter=months_filter
    )

@admin_bp.route('/reports/analytics/destinations')
@login_required
def analytics_destinations():
    # Get date range filter from query parameters
    months_filter = request.args.get('months', '12')
    try:
        months_filter = int(months_filter)
    except (ValueError, TypeError):
        months_filter = 12
    
    # Calculate the date range
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=30 * months_filter)
    
    # Get destination data for charts
    popular_destinations = (
        db.session.query(
            Tour.destination,
            Tour.title,
            func.count(Booking.id).label('booking_count')
        )
        .join(Booking, Tour.id == Booking.tour_id)
        .filter(Booking.booking_date >= start_date)
        .group_by(Tour.destination, Tour.title)
        .order_by(func.count(Booking.id).desc())
        .limit(10)
        .all()
    )
    
    # Format data for charts
    chart_data = {
        'labels': [dest.destination for dest in popular_destinations],
        'data': [dest.booking_count for dest in popular_destinations],
        'total_bookings': sum(dest.booking_count for dest in popular_destinations),
        'top_destination': popular_destinations[0].destination if popular_destinations else 'N/A'
    }
    
    return render_template(
        'admin/reports/analytics_destinations.html',
        chart_data=chart_data,
        popular_destinations=popular_destinations,
        now=datetime.datetime.utcnow(),
        months_filter=months_filter
    )
@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.admin_user_detail', user_id=user.id))
    return render_template('admin/edit_user.html', user_id=user_id, user=user, form=form)

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

@admin_bp.route('/admin/chatbot-settings', methods=['GET', 'POST'])
@login_required
def chatbot_settings():
    if not getattr(current_user, 'is_admin', False):
        abort(403)
    settings = ChatbotSettings.get_settings()
    if request.method == 'POST':
        api_key = request.form['groq_api_key']
        model = request.form['groq_model']
        if settings:
            settings.groq_api_key = api_key
            settings.groq_model = model
        else:
            settings = ChatbotSettings(groq_api_key=api_key, groq_model=model)
            db.session.add(settings)
        db.session.commit()
        flash('Chatbot settings updated!', 'success')
        return redirect(url_for('admin.chatbot_settings'))
    return render_template('admin/chatbot_settings.html', settings=settings)