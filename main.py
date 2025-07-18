from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
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
from models import User, Tour, Category, Destination, Booking, Review, TourDate
from forms import (TourForm, CategoryForm, TourSearchForm, BookingForm, PaymentForm, CancelForm,
                   ReviewForm, TourDateForm)
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
def book(tour_id):
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
                user_id=current_user.id if current_user.is_authenticated else None,
                special_requests=form.special_requests.data if hasattr(form, 'special_requests') else None
            )

            db.session.add(booking)
            db.session.commit()

            # ✅ Send Payment Confirmation Email instead of booking confirmation
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
    if form.validate_on_submit():
        tour = Tour()
        form.populate_obj(tour)
        # Handle image upload - FIXED to use featured_image
        if form.image.data:
            tour.featured_image = save_picture(form.image.data, 'tours')
        db.session.add(tour)
        db.session.commit()
        flash('Tour added successfully!', 'success')
        return redirect(url_for('admin_tours'))
    
    return render_template('admin/add_tour.html', form=form)

@app.route('/admin/edit-tour/<int:tour_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_tour(tour_id):
    if not current_user.is_admin:
        abort(403)
    
    tour = Tour.query.get_or_404(tour_id)
    form = TourForm(obj=tour)
    
    if form.validate_on_submit():
        form.populate_obj(tour)
        # Handle image upload - FIXED to use featured_image
        if form.image.data:
            tour.featured_image = save_picture(form.image.data, 'tours')
        db.session.commit()
        flash('Tour updated successfully!', 'success')
        return redirect(url_for('admin_tours'))
    
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