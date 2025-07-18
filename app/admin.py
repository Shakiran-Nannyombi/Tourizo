from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.Tour import Tour
from app.models.Category import Category
from app.forms import TourForm
from app.extensions import db
import logging
from app.models.Inquiry import Inquiry
from functools import wraps
from flask import make_response

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

def register_routes():
    @admin_bp.route('/dashboard')
    @login_required
    @nocache
    def dashboard():
        from sqlalchemy import func
        import datetime
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

register_routes()

@admin_bp.route('/inquiries')
def inquiries():
    all_inquiries = Inquiry.query.order_by(Inquiry.timestamp.desc()).all()
    return render_template('inquiries.html', inquiries=all_inquiries)

@admin_bp.route('/reports')
def reports():
    data = db.session.query(
        db.func.date(Inquiry.timestamp),
        db.func.count(Inquiry.id)
    ).group_by(db.func.date(Inquiry.timestamp)).all()

    chart_data = {
        "labels": [str(row[0]) for row in data],
        "counts": [row[1] for row in data]
    }

    return render_template('reports.html', chart_data=chart_data)

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
