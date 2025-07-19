from flask import Flask, current_app, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from sqlalchemy import extract, func
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from datetime import datetime, date
from PIL import Image
import os
import uuid
import secrets
import json
import requests
from app.auth import auth as auth_blueprint

from app.email_utils import send_cancellation_email, send_payment_success_email
from config import Config
from extensions import db, mail, moment
from flask_migrate import Migrate
from models import User, Tour, Category,Inquiry, Destination, Booking, Review, TourDate
from forms import (TourForm, CategoryForm, TourSearchForm, BookingForm, PaymentForm, CancelForm,
                   ReviewForm, TourDateForm, UserEditForm)
from forms import CancelForm, DeleteForm

app = Flask(__name__)

app.config.from_object(Config)
app.register_blueprint(auth_blueprint)

# Init extensions
db.init_app(app)
mail.init_app(app)
moment.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_categories():
    return dict(categories=Category.query.all())

@app.context_processor
def inject_moment():
    return dict(moment=moment)

def save_picture(form_picture, folder):
    if not form_picture:
        return None
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    upload_path = os.path.join(app.root_path, 'static', 'uploads', folder)
    os.makedirs(upload_path, exist_ok=True)
    picture_path = os.path.join(upload_path, picture_fn)
    img = Image.open(form_picture)
    img.thumbnail((800, 600))
    img.save(picture_path)
    return picture_fn

def generate_booking_reference():
    return 'TB' + str(uuid.uuid4()).replace('-', '')[:8].upper()

# ROUTES

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def index():
    featured_tours = Tour.query.filter_by(is_featured=True, is_active=True).limit(6).all()
    recent_tours = Tour.query.filter_by(is_active=True).order_by(Tour.created_at.desc()).limit(8).all()
    categories = Category.query.all()
    return render_template('index.html', featured_tours=featured_tours, recent_tours=recent_tours, categories=categories, current_time=datetime.utcnow())

@app.route('/tours')
def tours():
    form = TourSearchForm()
    search = request.args.get('search', '')
    destination = request.args.get('destination', '')
    category_id = request.args.get('category', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    page = request.args.get('page', 1, type=int)

    query = Tour.query.filter_by(is_active=True)
    if search:
        query = query.filter(Tour.title.contains(search) | Tour.description.contains(search))
    if destination:
        query = query.filter(Tour.destination.contains(destination))
    if category_id and category_id != 0:
        query = query.filter_by(category_id=category_id)
    if min_price:
        query = query.filter(Tour.price >= min_price)
    if max_price:
        query = query.filter(Tour.price <= max_price)

    tours = query.paginate(page=page, per_page=10, error_out=False)
    categories = Category.query.all()
    destinations = Destination.query.all()
    form.category.choices = [(0, 'All Categories')] + [(c.id, c.name) for c in categories]

    return render_template('tours.html', tours=tours, form=form, categories=categories, destinations=destinations, filters={
        'search': search,
        'destination': destination,
        'category': category_id,
        'min_price': min_price,
        'max_price': max_price
    })

@app.route('/tour/<int:tour_id>')
def tour_detail(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    image_list = []
    if tour.image_gallery:
        try:
            image_list = json.loads(tour.image_gallery)
        except Exception as e:
            print("Gallery parse error:", e)
    related_tours = Tour.query.filter(Tour.category_id == tour.category_id, Tour.id != tour.id).limit(4).all()
    reviews = Review.query.filter_by(tour_id=tour_id, is_approved=True).all()
    available_dates = TourDate.query.filter_by(tour_id=tour_id, is_available=True).all()
    return render_template('tour_detail.html', tour=tour, image_list=image_list, related_tours=related_tours, reviews=reviews, available_dates=available_dates)

# BOOKING ROUTES - FIXED

@app.route('/book', defaults={'tour_id': None}, methods=['GET', 'POST'])
@app.route('/book/<int:tour_id>', methods=['GET', 'POST'])
@login_required
def book(tour_id):
    # ✅ Check that only non-admins can book
    if current_user.role != 'user':
        flash("Only regular users can book tours. Admins are not allowed to book.", "warning")
        return redirect(url_for('welcome'))  # Or: redirect to user_dashboard or homepage

    # Get all tours and prices
    tours = Tour.query.all()
    tour_prices = {tour.id: float(tour.price) for tour in tours} if tours else {}
    form = BookingForm()

    # Populate tour choices
    form.tour_id.choices = [(tour.id, tour.title) for tour in tours]
    if tour_id:
        form.tour_id.data = tour_id

    if form.validate_on_submit():
        selected_tour = Tour.query.get(form.tour_id.data)
        if not selected_tour:
            flash('Selected tour not found.', 'error')
            return redirect(url_for('book'))

        try:
            payment_method = request.form.get('payment_method', 'momo')

            booking = Booking(
                reference=generate_booking_reference(),
                full_name=form.full_name.data,
                email=form.email.data,
                phone=form.phone.data,
                booking_date=form.booking_date.data,
                booking_time=form.booking_time.data,
                num_people=form.num_people.data,
                total_amount=float(selected_tour.price) * form.num_people.data,
                payment_method=payment_method,
                payment_status='paid',  # ✅ Mark as paid immediately
                tour_id=selected_tour.id,
                user_id=current_user.id,
                special_requests=form.special_requests.data if hasattr(form, 'special_requests') else None
            )

            db.session.add(booking)
            db.session.commit()

            # ✅ Send Payment Confirmation Email
            try:
                send_payment_success_email(
                    to_email=booking.email,
                    client_name=booking.full_name,
                    booking_reference=booking.reference,
                    total_amount=booking.total_amount,
                    payment_method=booking.payment_method,
                    payment_reference="TXN-Manual",
                    date=str(booking.booking_date),
                    time=str(booking.booking_time)
                )
            except Exception as e:
                print(f"Email error: {e}")

            flash(f'Booking confirmed and payment received! Reference: {booking.reference}', 'success')
            return redirect(url_for('my_bookings'))

        except Exception as e:
            db.session.rollback()
            print(f"Booking error: {e}")
            flash('An error occurred. Please try again.', 'error')

    elif request.method == 'POST':
        print("Form validation errors:", form.errors)
        flash("Please correct the errors in the form.", "warning")

    return render_template('bookings/book.html', form=form, tour_prices=tour_prices)

@app.route("/my-bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    cancel_form = CancelForm()
    delete_form = DeleteForm()
    payment_form = PaymentForm()
    return render_template("bookings/my_bookings.html",
                           bookings=bookings,
                           cancel_form=cancel_form,
                           delete_form=delete_form,
                           payment_form=payment_form)

@app.route('/cancel-booking/<int:booking_id>', methods=['GET', 'POST'])
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    form = CancelForm()

    if form.validate_on_submit():
        reason = form.reason.data
        notes = form.notes.data

        send_cancellation_email(
            to_email=booking.email,
            client_name=booking.full_name,
            booking_reference=booking.reference,
            total_amount=booking.total_amount,
            reason=reason,
            notes=notes,
            date=str(booking.booking_date),
            time=str(booking.booking_time),
            is_deletion=False
        )

        booking.payment_status = 'cancelled'  # ✅ Mark as cancelled instead of deleting
        db.session.commit()

        flash('Booking cancelled successfully.', 'success')
        return redirect(url_for('my_bookings'))

    return render_template('bookings/cancel_booking.html', booking=booking, form=form)

@app.route('/delete-booking/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    # Optional: check that the current user is the owner of the booking
    if booking.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    db.session.delete(booking)
    db.session.commit()

    flash('Booking deleted permanently.', 'success')
    return redirect(url_for('my_bookings'))



@app.route('/edit-booking/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    form = BookingForm(obj=booking)

    # ✅ Populate tour dropdown
    tours = Tour.query.all()
    form.tour_id.choices = [(tour.id, tour.title) for tour in tours]

    if request.method == 'GET':
        # ✅ Pre-fill payment_method and tour_id
        form.payment_method.data = booking.payment_method
        form.tour_id.data = booking.tour_id

    if form.validate_on_submit():
        # Update booking details
        booking.full_name = form.full_name.data
        booking.email = form.email.data
        booking.phone = form.phone.data
        booking.booking_date = form.booking_date.data
        booking.booking_time = form.booking_time.data
        booking.num_people = form.num_people.data
        booking.payment_method = request.form.get('payment_method', 'momo')  # Re-read from raw HTML if needed
        booking.special_requests = form.special_requests.data

        selected_tour = Tour.query.get(form.tour_id.data)
        if selected_tour:
            booking.tour_id = selected_tour.id
            booking.total_amount = float(selected_tour.price) * booking.num_people

        db.session.commit()
        flash('Booking updated successfully!', 'success')
        return redirect(url_for('my_bookings'))

    return render_template('bookings/edit_booking.html', form=form, booking=booking)


# ADMIN ROUTES
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    
    total_tours = Tour.query.count()
    total_bookings = Booking.query.count()
    total_users = User.query.count()
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_tours=total_tours,
                         total_bookings=total_bookings,
                         total_users=total_users,
                         recent_bookings=recent_bookings,
                         current_time=datetime.utcnow())

@app.route('/admin/tours')
@login_required
def admin_tours():
    if not current_user.is_admin:
        abort(403)
    tours = Tour.query.all()
    return render_template('admin/manage_tours.html', tours=tours)

@app.route('/admin/add-tour', methods=['GET', 'POST'])
@login_required
def admin_add_tour():
    if not current_user.is_admin:
        abort(403)
    
    form = TourForm()
    form.duration_type.choices = [
        ('Hours', 'Hours'),
        ('Days', 'Days'),
        ('Weeks', 'Weeks')
    ]

    form.difficulty_level.choices = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
        ('Expert', 'Expert')
    ]

    # Fetch categories from the database
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]

    if form.validate_on_submit():
        tour = Tour()
        form.populate_obj(tour)

        # Handle featured image upload
        if form.featured_image.data:
            tour.featured_image = save_picture(form.featured_image.data, 'tours')

        db.session.add(tour)
        db.session.commit()
        flash('Tour added successfully!', 'success')

        return redirect(url_for('admin_tours'))
    
    return render_template('admin/add_tour.html', form=form)

@app.route('/admin/edit-tour/<int:tour_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    
    # Debug: Print current tour data
    print(f"BEFORE UPDATE - Tour ID: {tour.id}, Title: {tour.title}")
    
    form = TourForm()
    
    # Set choices for SelectFields
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    form.difficulty_level.choices = [('Easy', 'Easy'), ('Moderate', 'Moderate'), ('Hard', 'Hard')]
    form.duration_type.choices = [('days', 'Days'), ('hours', 'Hours'), ('weeks', 'Weeks')]
    
    # For GET requests, populate form with existing data
    if request.method == 'GET':
        form.title.data = tour.title
        form.short_description.data = tour.short_description
        form.description.data = tour.description
        form.destination.data = tour.destination
        form.departure_location.data = tour.departure_location
        form.category_id.data = tour.category_id
        form.difficulty_level.data = tour.difficulty_level
        form.price.data = tour.price
        form.duration.data = tour.duration
        form.duration_type.data = tour.duration_type
        form.max_participants.data = tour.max_participants
        form.min_participants.data = tour.min_participants
        form.inclusions.data = tour.inclusions
        form.exclusions.data = tour.exclusions
        form.itinerary.data = tour.itinerary
        form.available_from.data = tour.available_from
        form.available_to.data = tour.available_to
        form.is_active.data = tour.is_active
        form.is_featured.data = tour.is_featured
        form.meta_title.data = tour.meta_title
        form.meta_description.data = tour.meta_description
    
    if request.method == 'POST':
        print("Form submitted!")
        print("Form validates:", form.validate_on_submit())
        if not form.validate_on_submit():
            print("Form errors:", form.errors)
    
    if form.validate_on_submit():
        print("Validation passed - updating tour...")
        
        # Debug: Print what we're about to update
        print(f"NEW TITLE: {form.title.data}")
        print(f"NEW DESCRIPTION: {form.description.data}")
        
        # Store old values for comparison
        old_title = tour.title
        old_description = tour.description
        
        # Populate model fields from form data
        tour.title = form.title.data
        tour.short_description = form.short_description.data
        tour.description = form.description.data
        tour.destination = form.destination.data
        tour.departure_location = form.departure_location.data
        tour.category_id = form.category_id.data
        tour.difficulty_level = form.difficulty_level.data
        tour.price = form.price.data
        tour.duration = form.duration.data
        tour.duration_type = form.duration_type.data
        tour.max_participants = form.max_participants.data
        tour.min_participants = form.min_participants.data
        tour.inclusions = form.inclusions.data
        tour.exclusions = form.exclusions.data
        tour.itinerary = form.itinerary.data
        tour.available_from = form.available_from.data
        tour.available_to = form.available_to.data
        tour.is_active = form.is_active.data
        tour.is_featured = form.is_featured.data
        tour.meta_title = form.meta_title.data
        tour.meta_description = form.meta_description.data
        
        # Debug: Check if values actually changed
        print(f"AFTER ASSIGNMENT - Title changed from '{old_title}' to '{tour.title}'")
        print(f"AFTER ASSIGNMENT - Description changed from '{old_description}' to '{tour.description}'")
        
        # Check if the object is dirty (has changes)
        print(f"Object dirty (has changes): {tour in db.session.dirty}")
        print(f"Object new: {tour in db.session.new}")
        
        # Handle file uploads if any
        if form.featured_image.data:
            print("Featured image uploaded")
            pass
        
        if form.gallery_images.data:
            print("Gallery images uploaded")
            pass
        
        try:
            print("About to commit to database...")
            db.session.commit()
            print("Database commit successful!")
            
            # Verify the changes were saved
            updated_tour = Tour.query.get(tour_id)
            print(f"AFTER COMMIT - Tour title in DB: {updated_tour.title}")
            
            flash('Tour updated successfully.', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating tour: {str(e)}', 'error')
            print("Database error:", str(e))
            import traceback
            traceback.print_exc()
    
    return render_template('admin/edit_tour.html', form=form, tour=tour)
@app.route('/review/<int:tour_id>', methods=['GET', 'POST'])
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
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(review)
        db.session.commit()
        flash('Thanks for your review! Awaiting approval.', 'success')
        return redirect(url_for('tour_detail', tour_id=tour_id))
    return render_template('add_review.html', tour=tour, form=form)
@app.route('/admin/inquiries')
@login_required
def admin_inquiries():
    if not current_user.is_admin:
        abort(403)
    inquiries = Inquiry.query.order_by(Inquiry.timestamp.desc()).all()
    return render_template('admin/manage_inquiries.html', inquiries=inquiries)

@app.route('/admin/inquiries/<int:inquiry_id>')
@login_required
def admin_inquiry_detail(inquiry_id):
    if not current_user.is_admin:
        abort(403)
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    return render_template('admin/inquiry_detail.html', inquiry=inquiry)

@app.route('/admin/inquiries/delete/<int:inquiry_id>', methods=['GET', 'POST'])
@login_required
def admin_inquiry_delete(inquiry_id):
    if not current_user.is_admin:
        abort(403)
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    if request.method == 'POST':
        db.session.delete(inquiry)
        db.session.commit()
        flash('Inquiry deleted successfully.', 'success')
        return redirect(url_for('admin_inquiries'))
    return render_template('admin/confirm_delete_inquiry.html', inquiry=inquiry)


@app.route('/pay', methods=['POST'])
@login_required
def pay():
    booking_id = request.form.get('booking_id')
    booking = Booking.query.get(booking_id)

    if not booking or booking.user_id != current_user.id:
        flash("Booking not found or access denied.", "error")
        return redirect(url_for('my_bookings'))

    # Update payment status
    booking.payment_status = 'paid'
    db.session.commit()

    # Send payment confirmation email
    send_payment_success_email(
        to_email=booking.email,
        client_name=booking.full_name,
        booking_reference=booking.reference,
        total_amount=booking.total_amount,
        payment_method="Manual",
        payment_reference="TXN12345",
        date=str(booking.booking_date),
        time=str(booking.booking_time)
    )

    flash(f"Payment successful for booking {booking.reference}!", "success")
    return redirect(url_for('my_bookings'))
@app.route('/submit_public_contact', methods=['POST'])
def submit_public_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    if not all([name, email, subject, message]):
        flash('Please fill in all fields', 'danger')
        return redirect(url_for('welcome'))  # or wherever your welcome page is routed

    try:
        msg = Message(
            subject=f"[Public Inquiry] {subject}",
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[current_app.config['ADMIN_EMAIL']],
            body=f"""
New message from the TravelMate Tours website:

Name: {name}
Email: {email}

Subject: {subject}

Message:
{message}
""")
        mail.send(msg)
        flash('Your message has been sent successfully!', 'success')
    except Exception as e:
        current_app.logger.error(f"Email send failed: {e}")
        flash('Error sending your message. Please try again.', 'danger')

    return redirect(url_for('welcome'))

@app.route('/admin/reports/bookings')
@login_required
def admin_booking_report():
    if not current_user.is_admin:
        abort(403)

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
    return render_template('admin/reports/bookings.html', bookings_by_month=bookings_by_month)


@app.route('/admin/reports/revenue')
@login_required
def admin_revenue_report():
    if not current_user.is_admin:
        abort(403)

    revenue_by_month = (
        db.session.query(
            extract('year', Booking.booking_date).label('year'),
            extract('month', Booking.booking_date).label('month'),
            func.sum(Booking.total_amount).label('total_revenue')
        )
        .filter(Booking.payment_status == 'paid')
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )
    return render_template('admin/reports/revenue.html', revenue_by_month=revenue_by_month)


@app.route('/admin/reports/popular-destinations')
@login_required
def admin_popular_destinations():
    if not current_user.is_admin:
        abort(403)

    popular_destinations = (
        db.session.query(
            Tour.destination,
            func.count(Booking.id).label('booking_count')
        )
        .join(Booking, Booking.tour_id == Tour.id)
        .filter(Booking.payment_status == 'paid')
        .group_by(Tour.destination)
        .order_by(func.count(Booking.id).desc())
        .limit(10)
        .all()
    )
    return render_template('admin/reports/popular_destinations.html', popular_destinations=popular_destinations)

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/manage_users.html', users=users)


@app.route('/admin/users/<int:user_id>')
@login_required
def admin_user_detail(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_detail.html', user=user)


@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)

    form = UserEditForm(obj=user)  # we'll define this form below

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin_users'))

    return render_template('admin/edit_user.html', form=form, user=user)


@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("You cannot delete your own account!", "warning")
        return redirect(url_for('admin_users'))

    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_users'))

# UTILITY FUNCTIONS
def send_booking_confirmation(booking):
    msg = Message(
        subject=f'Booking Confirmation - {booking.reference}',
        sender=app.config['MAIL_USERNAME'],
        recipients=[booking.email]
    )
    msg.body = f"""
    Dear {booking.full_name},

    Your booking has been confirmed!

    Booking Reference: {booking.reference}
    Tour: {booking.tour.title}
    Date: {booking.booking_date}
    Participants: {booking.num_people}
    Total Amount: ${booking.total_amount}

    We will contact you soon with further details.

    Thank you for choosing us!
    """
    mail.send(msg)

# ERROR HANDLERS
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403
if __name__ == '__main__':

    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='ssekiziyivugrace55@gmail.com',
                is_admin=True
            )
            admin.set_password('Ssekiziyivugrace@681')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")
        
        if not Category.query.first():
            categories = [
                Category(name='Adventure Tours'), 
                Category(name='Cultural Tours'), 
                Category(name='Beach Holidays')
            ]
            db.session.add_all(categories)
            db.session.commit()
        
        # Debug: Print all routes
        for rule in app.url_map.iter_rules():
            print(f"Endpoint: {rule.endpoint} | URL: {rule}")

    app.run(debug=True)