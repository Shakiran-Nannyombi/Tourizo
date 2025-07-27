# app/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response, jsonify
from app.forms import ProfileForm
from app.models.Booking import Booking
from app.models.Review import Review
from app.models.Inquiry import Inquiry
from app.forms import LoginForm, RegistrationForm

from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.User import User
from app.extensions import db, mail
from flask_mail import Message
from functools import wraps
from datetime import datetime, timedelta
import re
import secrets
import string
import random
from urllib.parse import urlparse, urljoin
import json

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
contact = Blueprint('contact', __name__)


# Utility Functions
def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_safe_url(target):
    """Check if the redirect URL is safe (same domain)"""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    """Get the redirect target from request args or referrer"""
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target
    return None


def nocache(view):
    """Prevent browser caching of certain views"""
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return no_cache


def generate_unique_username(first_name, last_name):
    """Generate a unique username from first and last name"""
    base_username = f"{first_name.lower()}{last_name.lower()}"
    username = ''.join(c for c in base_username if c.isalnum())
    
    # Ensure minimum length
    if len(username) < 3:
        username = f"user{username}"
    
    # Check for uniqueness and add suffix if needed
    original_username = username
    suffix = 1
    while User.query.filter(User.username.ilike(username)).first():
        username = f"{original_username}{suffix}"
        suffix += 1
    
    return username


def send_otp_email(email, otp):
    """Send OTP via email"""
    try:
        msg = Message('Password Reset OTP', recipients=[email])
        msg.body = f"""
        Your password reset OTP is: {otp}
        
        This code will expire in 15 minutes.
        
        If you didn't request this password reset, please ignore this email.
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {email}: {e}")
        return False


# Authentication Routes

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login with comprehensive error handling and redirect support"""
    # Redirect if already logged in
    if current_user.is_authenticated:
        # Check for pending redirect
        next_page = request.args.get('next')
        if next_page and is_safe_url(next_page):
            return redirect(next_page)
        elif current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('auth.user_dashboard'))
    
    if request.method == 'POST':
        # Get form data with proper cleaning
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))
        
        print("🔍 LOGIN ATTEMPT DEBUG:")
        print(f"   Email: '{email}'")
        print(f"   Password length: {len(password) if password else 0}")
        print(f"   Remember me: {remember}")
        print(f"   Next parameter: {request.args.get('next')}")
        
        # Basic validation
        if not email or not password:
            print("❌ Email or password is empty")
            flash('Please enter both email and password.', 'danger')
            return render_template('auth/login.html')
        
        if not is_valid_email(email):
            print(f"❌ Invalid email format: {email}")
            flash('Please enter a valid email address.', 'danger')
            return render_template('auth/login.html')
        
        # Find user by email (case-insensitive)
        user = User.query.filter(User.email.ilike(email)).first()
        
        if user:
            print(f"✅ User found: {user.username} ({user.email})")
            
            try:
                if user.check_password(password):
                    print("✅ Password is correct - logging in user")
                    
                    # Update hash format if needed (for legacy compatibility)
                    try:
                        if hasattr(user, 'update_password_hash_if_needed'):
                            user.update_password_hash_if_needed(password)
                    except Exception as hash_update_error:
                        print(f"⚠ Hash update failed: {hash_update_error}")
                    
                    # Log the user in
                    login_success = login_user(user, remember=remember)
                    
                    if login_success:
                        flash('Login successful! Welcome back.', 'success')
                        
                        # Enhanced redirect logic
                        next_page = request.args.get('next')
                        if next_page and is_safe_url(next_page):
                            print(f"✅ Redirecting to: {next_page}")
                            return redirect(next_page)
                        elif user.is_admin:
                            return redirect(url_for('admin.dashboard'))
                        else:
                            return redirect(url_for('auth.user_dashboard'))
                    else:
                        print("❌ Flask-Login failed")
                        flash('Login failed. Please try again.', 'danger')
                else:
                    print("❌ Password is incorrect")
                    flash('Invalid email or password.', 'danger')
                    
            except Exception as password_error:
                            print(f"❌ Password check exception: {password_error}")
            flash('An error occurred during login. Please try again.', 'danger')
        else:
            print(f"❌ No user found with email: {email}")
            flash('Invalid email or password.', 'danger')
    
    # GET request - pass next parameter to template
    next_page = request.args.get('next')
    return render_template('auth/login.html', next=next_page)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with comprehensive validation and redirect support"""
    if current_user.is_authenticated:
        # Check for pending redirect
        next_page = request.args.get('next')
        if next_page and is_safe_url(next_page):
            return redirect(next_page)
        elif current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('auth.user_dashboard'))
    
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        username_input = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        print("🔍 REGISTRATION ATTEMPT:")
        print(f"   First Name: '{first_name}'")
        print(f"   Last Name: '{last_name}'")
        print(f"   Username Input: '{username_input}'")
        print(f"   Email: '{email}'")
        print(f"   Phone: '{phone}'")
        print(f"   Next parameter: {request.args.get('next')}")
        
        # Validation
        errors = []
        
        # Check required fields
        if not first_name or len(first_name) < 2:
            errors.append('First name must be at least 2 characters long.')
        
        if not last_name or len(last_name) < 2:
            errors.append('Last name must be at least 2 characters long.')
        
        if not email or not is_valid_email(email):
            errors.append('Please enter a valid email address.')
        
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        # Combine first_name and last_name as username if no username input provided
        if username_input:
            username = username_input
            if len(username) < 3:
                errors.append('Username must be at least 3 characters long.')
        else:
            username = f"{first_name} {last_name}".strip()
        
        # Check for existing users
        if User.query.filter(User.username.ilike(username)).first():
            errors.append('Username already exists.')
        
        if User.query.filter(User.email.ilike(email)).first():
            errors.append('Email already registered.')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html', next=request.args.get('next'))
        
        try:
            # Create new user with combined username, no first_name/last_name fields
            user = User(
                username=username,
                email=email
            )
            
            # Add phone if field exists in model
            if hasattr(user, 'phone') and phone:
                user.phone = phone
            
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            print(f"✅ User registered successfully: {email}")
            
            # Auto-login after registration
            login_user(user)
            session['new_user'] = True
            
            flash('Registration successful! Welcome to the platform.', 'success')
            
            # Enhanced redirect logic after registration
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                print(f"✅ Redirecting new user to: {next_page}")
                return redirect(next_page)
            elif user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('auth.user_dashboard'))
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Registration error: {e}")
            flash('An error occurred during registration. Please try again.', 'danger')
    
    # GET request - pass next parameter to template
    next_page = request.args.get('next')
    return render_template('auth/register.html', next=next_page)


@auth_bp.route('/user/dashboard')
@login_required
def user_dashboard():
    username = current_user.username
    user_bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    return render_template('user_dashboard.html', username=username, bookings=user_bookings)


@contact.route('/contact', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        contact_method = request.form.get('contact_method')
        travelers = request.form.get('travelers')
        country = request.form.get('country')
        message = request.form.get('message')

        # TODO: Save to DB or send email here

        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact.contact_form'))

    return render_template('contact.html')


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        
        # Handle additional fields from the form
        date_of_birth = request.form.get('date_of_birth')
        if date_of_birth:
            try:
                current_user.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        current_user.bio = request.form.get('bio', '')
        
        if form.password.data:
            current_user.password_hash = generate_password_hash(form.password.data)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    
    return render_template('profile.html', form=form)


@auth_bp.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@auth_bp.route('/settings/save', methods=['POST'])
@login_required
def save_settings():
    try:
        # For now, just return success since the database fields don't exist yet
        # In a real implementation, you would update the user's settings here
        # current_user.email_notifications = request.form.get('email_notifications') == 'on'
        # current_user.newsletter = request.form.get('newsletter') == 'on'
        # current_user.sms_notifications = request.form.get('sms_notifications') == 'on'
        # current_user.language = request.form.get('language', 'en')
        # current_user.timezone = request.form.get('timezone', 'UTC')
        # current_user.two_factor_auth = request.form.get('two_factor_auth') == 'on'
        # current_user.public_profile = request.form.get('public_profile') == 'on'
        # db.session.commit()
        
        return jsonify({'success': True, 'message': 'Settings saved successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@auth_bp.route('/settings/change-password', methods=['POST'])
@login_required
def change_password():
    try:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Verify current password
        if not check_password_hash(current_user.password_hash, current_password):
            return jsonify({'success': False, 'message': 'Current password is incorrect'})
        
        # Check if new passwords match
        if new_password != confirm_password:
            return jsonify({'success': False, 'message': 'New passwords do not match'})
        
        # Update password
        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Password changed successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@auth_bp.route('/settings/export-data')
@login_required
def export_data():
    try:
        # Prepare user data for export
        user_data = {
            'user_info': {
                'username': current_user.username,
                'email': current_user.email,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'phone': current_user.phone,
                'date_of_birth': current_user.date_of_birth.isoformat() if current_user.date_of_birth else None,
                'bio': current_user.bio,
                'date_created': current_user.date_created.isoformat() if current_user.date_created else None,
                'last_login': current_user.last_login.isoformat() if current_user.last_login else None
            },
            'settings': {
                'email_notifications': current_user.email_notifications,
                'newsletter': current_user.newsletter,
                'sms_notifications': current_user.sms_notifications,
                'language': current_user.language,
                'timezone': current_user.timezone,
                'two_factor_auth': current_user.two_factor_auth,
                'public_profile': current_user.public_profile
            },
            'bookings': [
                {
                    'tour_name': booking.tour.name if booking.tour else 'N/A',
                    'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
                    'status': booking.status,
                    'amount': float(booking.amount) if booking.amount else 0
                }
                for booking in current_user.bookings
            ],
            'reviews': [
                {
                    'tour_name': review.tour.name if review.tour else 'N/A',
                    'rating': review.rating,
                    'comment': review.comment,
                    'created_at': review.created_at.isoformat() if review.created_at else None
                }
                for review in current_user.reviews
            ]
        }
        
        # Create JSON response
        response = jsonify(user_data)
        response.headers['Content-Disposition'] = 'attachment; filename=user-data.json'
        return response
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@auth_bp.route('/settings/delete-account', methods=['POST'])
@login_required
def delete_account():
    try:
        # Delete user's bookings
        Booking.query.filter_by(user_id=current_user.id).delete()
        
        # Delete user's reviews
        Review.query.filter_by(user_id=current_user.id).delete()
        
        # Delete user's inquiries
        Inquiry.query.filter_by(user_id=current_user.id).delete()
        
        # Delete user
        db.session.delete(current_user)
        db.session.commit()
        
        logout_user()
        return jsonify({'success': True, 'message': 'Account deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@auth_bp.route('/logout')
@login_required
@nocache
def logout():
    """Enhanced logout with complete session cleanup"""
    print(f"🚪 User {current_user.username} logging out")
    
    # Store user info before logout for flash message
    username = current_user.username
    
    # Logout user
    logout_user()
    
    # Clear all session data
    session.clear()
    
    # Create response with redirect
    response = make_response(redirect(url_for('welcome')))
    
    # Clear authentication cookies
    response.delete_cookie('remember_token')
    response.delete_cookie('session')
    
    # Add cache control headers to prevent back button issues
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    
    flash(f'You have been logged out successfully, {username}. Come back soon!', 'info')
    print(f"✅ User {username} logged out successfully")
    
    return response


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Password reset request with OTP generation"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if not email or not is_valid_email(email):
            flash('Please enter a valid email address.', 'danger')
            return render_template('auth/forgot_password.html')
        
        user = User.query.filter(User.email.ilike(email)).first()
        
        if user:
            # Generate secure OTP
            otp = ''.join(secrets.choice(string.digits) for _ in range(6))
            user.otp_code = otp
            user.otp_expiry = datetime.utcnow() + timedelta(minutes=15)
            
            try:
                db.session.commit()
                
                # Send OTP via email
                if send_otp_email(email, otp):
                    flash('A password reset code has been sent to your email.', 'success')
                else:
                    # Fallback: show OTP in debug mode (remove in production)
                    print(f"🔑 OTP for {email}: {otp}")
                    flash(f'Password reset code sent. (Debug: {otp})', 'info')
                
                return redirect(url_for('auth.reset_password', email=email))
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ OTP generation error: {e}")
                flash('An error occurred. Please try again.', 'danger')
        else:
            # Security: Don't reveal if email exists
            flash('If an account with that email exists, a reset code has been sent.', 'info')
    
    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Password reset with OTP verification"""
    email = request.args.get('email') or request.form.get('email')
    user = User.query.filter(User.email.ilike(email)).first() if email else None
    
    if request.method == 'POST':
        # Handle OTP resend
        if 'resend_otp' in request.form and user:
            otp = ''.join(secrets.choice(string.digits) for _ in range(6))
            user.otp_code = otp
            user.otp_expiry = datetime.utcnow() + timedelta(minutes=15)
            
            try:
                db.session.commit()
                
                if send_otp_email(email, otp):
                    flash('A new reset code has been sent to your email.', 'success')
                else:
                    print(f"🔑 New OTP for {email}: {otp}")
                    flash(f'New reset code sent. (Debug: {otp})', 'info')
                
                return render_template('auth/reset_password.html', email=email)
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ OTP resend error: {e}")
                flash('An error occurred while resending the code.', 'danger')
        
        # Handle password reset
        else:
            otp = request.form.get('otp', '').strip()
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            if not user:
                flash('Invalid email address.', 'danger')
                return redirect(url_for('auth.forgot_password'))
            
            if not all([otp, new_password, confirm_password]):
                flash('All fields are required.', 'danger')
                return render_template('auth/reset_password.html', email=email)
            
            if new_password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('auth/reset_password.html', email=email)
            
            if len(new_password) < 6:
                flash('Password must be at least 6 characters long.', 'danger')
                return render_template('auth/reset_password.html', email=email)
            
            # Verify OTP
            if (user.otp_code == otp and 
                user.otp_expiry and 
                user.otp_expiry > datetime.utcnow()):
                
                try:
                    user.set_password(new_password)
                    user.otp_code = None
                    user.otp_expiry = None
                    db.session.commit()
                    
                    flash('Password reset successful! Please log in with your new password.', 'success')
                    return redirect(url_for('auth.login'))
                    
                except Exception as e:
                    db.session.rollback()
                    print(f"❌ Password reset error: {e}")
                    flash('An error occurred while resetting your password.', 'danger')
            else:
                flash('Invalid or expired reset code.', 'danger')
    
    return render_template('auth/reset_password.html', email=email)


# Debug Routes (REMOVE IN PRODUCTION)
@auth_bp.route('/debug/users')
def debug_users():
    """Debug route to see all users - REMOVE IN PRODUCTION"""
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        return "Access denied", 403
    
    users = User.query.all()
    output = "<h1>Debug: All Users</h1>"
    output += f"<p>Total users: {len(users)}</p>"
    
    for user in users:
        output += f"""
        <div style='border: 1px solid #ccc; margin: 10px; padding: 10px;'>
            <strong>ID:</strong> {user.id}<br>
            <strong>Username:</strong> {user.username}<br>
            <strong>Email:</strong> {user.email}<br>
            <strong>Name:</strong> {getattr(user, 'first_name', 'N/A')} {getattr(user, 'last_name', 'N/A')}<br>
            <strong>Phone:</strong> {getattr(user, 'phone', 'N/A')}<br>
            <strong>Hash:</strong> {user.password_hash[:50]}...<br>
            <strong>Is Admin:</strong> {getattr(user, 'is_admin', False)}<br>
            <strong>Created:</strong> {getattr(user, 'created_at', 'N/A')}<br>
            <strong>OTP:</strong> {getattr(user, 'otp_code', 'None')} 
            (Expires: {getattr(user, 'otp_expiry', 'N/A')})<br>
        </div>
        """
    
    return output


@auth_bp.route('/debug/create-test-user')
def create_test_user():
    """Create a test user for debugging - REMOVE IN PRODUCTION"""
    try:
        # Check if test user already exists
        existing_user = User.query.filter(User.email.ilike('test@example.com')).first()
        if existing_user:
            return f"Test user already exists: test@example.com (ID: {existing_user.id})"
        
        # Create test user
        if hasattr(User, 'create_test_user'):
            test_user = User.create_test_user('testuser', 'test@example.com', 'password123')
        else:
            test_user = User(
                username='testuser',
                email='test@example.com',
                first_name='Test',
                last_name='User'
            )
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
        
        return f"Test user created: test@example.com / password123 (ID: {test_user.id})"
        
    except Exception as e:
        db.session.rollback()
        return f"Error creating test user: {e}"


@auth_bp.route('/debug/clear-otp/<int:user_id>')
def clear_user_otp(user_id):
    """Clear OTP for a specific user - REMOVE IN PRODUCTION"""
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        return "Access denied", 403
    
    try:
        user = User.query.get(user_id)
        if user:
            user.otp_code = None
            user.otp_expiry = None
            db.session.commit()
            return f"OTP cleared for user: {user.email}"
        else:
            return "User not found"
    except Exception as e:
        db.session.rollback()
        return f"Error clearing OTP: {e}"