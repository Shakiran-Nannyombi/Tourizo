from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message

# Initialize SQLAlchemy
from extensions import db, mail, moment
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import json
import uuid
from datetime import datetime, date
from PIL import Image
import secrets
from config import Config
from flask_moment import Moment
from models import Destination
from flask_migrate import Migrate
import json
from datetime import datetime


# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
mail.init_app(app)
moment.init_app(app)

# Initialize Flask-Migrate
from flask_migrate import Migrate
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Import models after db initialization
from models import User, Tour, Category, Booking, Review, TourDate
from forms import (TourForm, CategoryForm, TourSearchForm, BookingForm, 
                   ReviewForm, TourDateForm)

@app.context_processor
def inject_categories():
    """Make categories available in all templates"""
    return dict(categories=Category.query.all())

@app.context_processor
def inject_moment():
    """Make flask-moment available in templates"""
    return dict(moment=moment)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def save_picture(form_picture, folder):
    """Save uploaded picture and return filename"""
    if not form_picture:
        return None
    
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    upload_path = os.path.join(app.root_path, 'static', 'uploads', folder)
    os.makedirs(upload_path, exist_ok=True)
    
    picture_path = os.path.join(upload_path, picture_fn)
    
    output_size = (800, 600)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    
    return picture_fn

def generate_booking_reference():
    """Generate unique booking reference"""
    return 'TB' + str(uuid.uuid4()).replace('-', '')[:8].upper()

# ====================== ROUTES ======================
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/')
def index():
    featured_tours = Tour.query.filter_by(is_featured=True, is_active=True).limit(6).all()
    recent_tours = Tour.query.filter_by(is_active=True).order_by(Tour.created_at.desc()).limit(8).all()
    categories = Category.query.all()
    
    return render_template('index.html', 
                         featured_tours=featured_tours,
                         recent_tours=recent_tours,
                         categories=categories,
                         current_time=datetime.utcnow())

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
        # Fixed: Use .title instead of .name since that's what's in your model
        query = query.filter(
            Tour.title.contains(search) | 
            Tour.description.contains(search)
        )
    
    if destination:
        # Fixed: Use the destination string field
        query = query.filter(Tour.destination.contains(destination))
    
    if category_id and category_id != 0:
        query = query.filter_by(category_id=category_id)
    
    if min_price:
        query = query.filter(Tour.price >= min_price)
    
    if max_price:
        query = query.filter(Tour.price <= max_price)
    
    tours = query.paginate(page=page, per_page=app.config.get('TOURS_PER_PAGE', 10), error_out=False)
    categories = Category.query.all()
    destinations = Destination.query.all()
    
    form.category.choices = [(0, 'All Categories')] + [(c.id, c.name) for c in categories]
    
    return render_template(
        'tours.html',
        tours=tours,
        form=form,
        categories=categories,
        destinations=destinations,
        filters={
            'search': search,
            'destination': destination,
            'category': category_id,
            'min_price': min_price,
            'max_price': max_price
        }
    )


@app.route('/tour/<int:tour_id>')
def tour_detail(tour_id):
    tour = Tour.query.get_or_404(tour_id)

    # ✅ Convert image_gallery JSON string to list
    image_list = []
    if tour.image_gallery:
        try:
            image_list = json.loads(tour.image_gallery)
        except Exception as e:
            print("Failed to parse image_gallery:", e)

    related_tours = Tour.query.filter(
        Tour.category_id == tour.category_id,
        Tour.id != tour.id
    ).limit(4).all()

    reviews = Review.query.filter_by(tour_id=tour_id, is_approved=True).all()
    available_dates = TourDate.query.filter_by(tour_id=tour_id, is_available=True).all()

    return render_template(
        'tour_detail.html',
        tour=tour,
        image_list=image_list,  # ✅ Pass decoded list to template
        related_tours=related_tours,
        reviews=reviews,
        available_dates=available_dates
    )
@app.route('/book/<int:tour_id>', methods=['GET', 'POST'])
def book_tour(tour_id):
    """Book a tour package"""
    tour = Tour.query.get_or_404(tour_id)
    form = BookingForm()
    
    if form.validate_on_submit():
        # Create booking
        booking = Booking(
            booking_reference=generate_booking_reference(),
            customer_name=form.customer_name.data,
            customer_email=form.customer_email.data,
            customer_phone=form.customer_phone.data,
            tour_date=form.tour_date.data,
            participants=form.participants.data,
            total_amount=tour.price * form.participants.data,
            special_requests=form.special_requests.data,
            tour_id=tour_id,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        
        db.session.add(booking)
        db.session.commit()
        
        # Send confirmation email
        try:
            send_booking_confirmation(booking)
        except Exception:
            flash('Booking created but email notification failed.', 'warning')
        
        flash(f'Booking confirmed! Reference: {booking.booking_reference}', 'success')
        return redirect(url_for('booking_success', booking_id=booking.id))
    
    return render_template('book_tour.html', tour=tour, form=form)



@app.route('/booking-success/<int:booking_id>')
def booking_success(booking_id):
    """Booking success page"""
    booking = Booking.query.get_or_404(booking_id)
    return render_template('booking_success.html', booking=booking)

@app.route('/review/<int:tour_id>', methods=['GET', 'POST'])
def add_review(tour_id):
    """Add review for a tour"""
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
        
        flash('Thank you for your review! It will be published after moderation.', 'success')
        return redirect(url_for('tour_detail', tour_id=tour_id))  # ✅ fixed here
    
    return render_template('add_review.html', tour=tour, form=form)

# Admin Routes
# Dummy decorator
#def no_login_required(f):
    #return f

# Use instead of @login_required
#@no_login_required
@app.route('/admin')
def admin_dashboard():
    ...

    """Admin dashboard"""
    #if not current_user.is_admin:
     #   abort(403)
    
    # Get statistics
    total_tours = Tour.query.count()
    active_tours = Tour.query.filter_by(is_active=True).count()
    total_bookings = Booking.query.count()
    pending_bookings = Booking.query.filter_by(status='pending').count()
    total_reviews = Review.query.count()
    pending_reviews = Review.query.filter_by(is_approved=False).count()
    
    # Recent bookings
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    
    # Popular tours
    popular_tours = db.session.query(Tour, db.func.count(Booking.id).label('booking_count'))\
        .join(Booking)\
        .group_by(Tour.id)\
        .order_by(db.func.count(Booking.id).desc())\
        .limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_tours=total_tours,
                         active_tours=active_tours,
                         total_bookings=total_bookings,
                         pending_bookings=pending_bookings,
                         total_reviews=total_reviews,
                         pending_reviews=pending_reviews,
                         recent_bookings=recent_bookings,
                         popular_tours=popular_tours,
                         current_time=datetime.now() 
                         )


@app.route('/admin/tours')
#@no_login_required
def admin_tours():
    """Admin tour management"""
    

   # if not current_user.is_admin:
      #  abort(403)

       
    page = request.args.get('page', 1, type=int)
    tours = Tour.query.order_by(Tour.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/manage_tours.html', tours=tours)

@app.route('/admin/tours/add', methods=['GET', 'POST'])
def admin_add_tour():
    """Add new tour package"""
    form = TourForm()
    categories = Category.query.all()
    destinations = Destination.query.all()
    
    # Set up form choices
    form.category_id.choices = [(c.id, c.name) for c in categories]
    #form.destination.choices = [(d.id, d.name) for d in destinations]  # Use destination_id
    #form.departure_location.choices = [('Kampala', 'Kampala'), ('Entebbe', 'Entebbe')]
    form.duration_type.choices = [('Days', 'Days'), ('Nights', 'Nights')]
    form.difficulty_level.choices = [('Easy', 'Easy'), ('Moderate', 'Moderate'), ('Hard', 'Hard')]
    
    if form.validate_on_submit():
        try:
            # Save featured image
            featured_image_filename = None
            if form.featured_image.data:
                featured_image_filename = save_picture(form.featured_image.data, 'tours')
            
            # Save gallery images
            gallery_images = []
            if form.gallery_images.data:
                for image in form.gallery_images.data:
                    if image:
                        filename = save_picture(image, 'tours')
                        if filename:
                            gallery_images.append(filename)
            
            # Create tour - Fix field names to match your Tour model
            tour = Tour(
                title=form.title.data,  # Make sure this matches your model field
                short_description=form.short_description.data,
                description=form.description.data,
                destination=form.destination.data,  # Use destination_id, not destination
                departure_location=form.departure_location.data,
                category_id=form.category_id.data,
                price=form.price.data,
                duration=form.duration.data,
                duration_type=form.duration_type.data,
                max_participants=form.max_participants.data,
                min_participants=form.min_participants.data,
                difficulty_level=form.difficulty_level.data,
                featured_image=featured_image_filename,
                image_gallery=json.dumps(gallery_images),
                inclusions=form.inclusions.data,
                exclusions=form.exclusions.data,
                itinerary=form.itinerary.data,
                available_from=form.available_from.data,
                available_to=form.available_to.data,
                is_active=form.is_active.data,
                is_featured=form.is_featured.data,
                meta_title=form.meta_title.data,
                meta_description=form.meta_description.data
                
            )
            
            db.session.add(tour)
            db.session.commit()
            
            flash('Tour package added successfully!', 'success')
            return redirect(url_for('admin_tours'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding tour: {str(e)}', 'error')
            print(f"Error: {e}")  # For debugging
    
    else:
        # Debug form validation errors
        if request.method == 'POST':
            print("Form validation failed:")
            for field, errors in form.errors.items():
                print(f"{field}: {errors}")
    
    return render_template('admin/add_tour.html', form=form)

@app.route('/admin/tours/edit/<int:id>', methods=['GET', 'POST'])
def admin_edit_tour(id):
    """Edit tour package"""
    tour = Tour.query.get_or_404(id)
    form = TourForm(obj=tour)
    
    # Set choices dynamically for select fields
    categories = Category.query.all()
    destinations = Destination.query.all()
    
    form.category_id.choices = [(c.id, c.name) for c in categories]
    #form.destination.choices = [(d.id, d.name) for d in destinations]
    #form.departure_location.choices = [('Kampala', 'Kampala'), ('Entebbe', 'Entebbe')]
    form.duration_type.choices = [('Days', 'Days'), ('Nights', 'Nights')]
    form.difficulty_level.choices = [('Easy', 'Easy'), ('Moderate', 'Moderate'), ('Hard', 'Hard')]

    if form.validate_on_submit():
        try:
            # Handle featured image
            if form.featured_image.data:
                featured_image_filename = save_picture(form.featured_image.data, 'tours')
                tour.featured_image = featured_image_filename

            # Handle gallery images
            if form.gallery_images.data:
                gallery_images = []
                for image in form.gallery_images.data:
                    if image:
                        filename = save_picture(image, 'tours')
                        if filename:
                            gallery_images.append(filename)
                tour.image_gallery = json.dumps(gallery_images)

            # Update tour fields
            tour.title = form.title.data
            tour.short_description = form.short_description.data
            tour.description = form.description.data
            tour.destination = form.destination.data  # Use destination
            tour.departure_location = form.departure_location.data
            tour.category_id = form.category_id.data
            tour.price = form.price.data
            tour.duration = form.duration.data
            tour.duration_type = form.duration_type.data
            tour.max_participants = form.max_participants.data
            tour.min_participants = form.min_participants.data
            tour.difficulty_level = form.difficulty_level.data
            tour.inclusions = form.inclusions.data
            tour.exclusions = form.exclusions.data
            tour.itinerary = form.itinerary.data
            tour.available_from = form.available_from.data
            tour.available_to = form.available_to.data
            tour.is_active = form.is_active.data
            tour.is_featured = form.is_featured.data
            tour.meta_title = form.meta_title.data
            tour.meta_description = form.meta_description.data
            tour.updated_at = datetime.utcnow()

            db.session.commit()
            flash('Tour package updated successfully!', 'success')
            return redirect(url_for('admin_tours'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating tour: {str(e)}', 'error')
            print(f"Error: {e}")
    
    else:
        # Debug form validation errors
        if request.method == 'POST':
            print("Form validation failed:")
            for field, errors in form.errors.items():
                print(f"{field}: {errors}")
    
    return render_template('admin/edit_tour.html', form=form, tour=tour)

@app.route('/admin/tours/delete/<int:id>', methods=['POST'])
#@login_required
def admin_delete_tour(id):
    """Delete tour package"""
    #if not current_user.is_admin:
      #  abort(403)
    
    tour = Tour.query.get_or_404(id)
    
    # Check if tour has bookings
    if tour.bookings:
        flash('Cannot delete tour with existing bookings. Deactivate instead.', 'error')
        return redirect(url_for('admin_tours'))
    
    db.session.delete(tour)
    db.session.commit()
    
    flash('Tour package deleted successfully!', 'success')
    return redirect(url_for('admin_tours'))

@app.route('/admin/categories')
#@login_required
def admin_categories():
    """Manage categories"""
    #if not current_user.is_admin:
       # abort(403)
    
    categories = Category.query.all()
    return render_template('admin/manage_categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
#@login_required
def admin_add_category():
    """Add new category"""
   # if not current_user.is_admin:
      #  abort(403)
    
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('Category added successfully!', 'success')
        return redirect(url_for('admin_categories'))
    
    return render_template('admin/add_category.html', form=form)

@app.route('/admin/bookings')
#@login_required
def admin_bookings():
    """Manage bookings"""
  #  if not current_user.is_admin:
      #  abort(403)
    
    page = request.args.get('page', 1, type=int)
    bookings = Booking.query.order_by(Booking.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/manage_bookings.html', bookings=bookings)

@app.route('/admin/bookings/update-status/<int:booking_id>', methods=['POST'])
#@login_required
def admin_update_booking_status(booking_id):
    """Update booking status"""
   # if not current_user.is_admin:
      #  abort(403)
    
    booking = Booking.query.get_or_404(booking_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'confirmed', 'cancelled', 'completed']:
        booking.status = new_status
        booking.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash(f'Booking status updated to {new_status}', 'success')
    else:
        flash('Invalid status', 'error')
    
    return redirect(url_for('admin_bookings'))

# Email functions
def send_booking_confirmation(booking):
    """Send booking confirmation email"""
    msg = Message(
        subject=f'Booking Confirmation - {booking.booking_reference}',
        sender=app.config['MAIL_USERNAME'],
        recipients=[booking.customer_email]
    )
    
    msg.body = f"""
    Dear {booking.customer_name},
    
    Your booking has been confirmed!
    
    Booking Reference: {booking.booking_reference}
    Tour: {booking.tour.title}
    Date: {booking.tour_date}
    Participants: {booking.participants}
    Total Amount: ${booking.total_amount}
    
    We will contact you soon with further details.
    
    Thank you for choosing us!
    """
    
    mail.send(msg)

# Error handlers
app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

# ====================== MAIN ======================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
        
        if not Category.query.first():
            categories = [
                Category(name='Adventure Tours'),
                Category(name='Cultural Tours'),
                Category(name='Beach Holidays')
            ]
            db.session.add_all(categories)
            db.session.commit()
    
    app.run(debug=True)