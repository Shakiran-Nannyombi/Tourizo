from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.User import User
from app.extensions import db
from functools import wraps
from flask import make_response
from datetime import datetime, timedelta
import random
import string
from app.extensions import mail
from flask_mail import Message

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

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def register_routes():
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Logged in successfully!', 'success')
                if user.is_admin:
                    return redirect(url_for('admin.dashboard'))
                else:
                    return redirect(url_for('auth.user_dashboard'))
            else:
                flash('Invalid email or password', 'danger')
        return render_template('login.html')

    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'danger')
            elif User.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
            else:
                user = User(username=username, email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                session['new_user'] = True
                flash('Registration successful! You are now logged in.', 'success')
                if user.is_admin:
                    return redirect(url_for('admin.dashboard'))
                else:
                    return redirect(url_for('auth.user_dashboard'))
        return render_template('register.html')

    @auth_bp.route('/profile')
    @login_required
    def profile():
        return 'Profile Page (to be implemented)'

    @auth_bp.route('/user_dashboard')
    @login_required
    @nocache
    def user_dashboard():
        is_new_user = session.pop('new_user', False)
        return render_template('user_dashboard.html', username=current_user.username, is_new_user=is_new_user)

    @auth_bp.route('/logout')
    @login_required
    def logout():
        logout_user()
        session.clear()  # Clear all session data for extra security
        flash('You have been logged out.', 'info')
        return redirect(url_for('welcome'))

    @auth_bp.route('/forgot-password', methods=['GET', 'POST'])
    def forgot_password():
        from flask import flash, redirect, url_for, request, render_template
        from app.models.User import User
        from app.extensions import db, mail
        from flask_mail import Message
        if request.method == 'POST':
            email = request.form.get('email')
            user = User.query.filter_by(email=email).first()
            if user:
                otp = ''.join(random.choices(string.digits, k=6))
                user.otp_code = otp
                user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
                db.session.commit()
                # Send OTP via email
                msg = Message('Tourizo Password Reset OTP', recipients=[email])
                msg.body = f"Your Tourizo OTP is: {otp}\nThis code will expire in 10 minutes."
                mail.send(msg)
                flash('A one-time password (OTP) has been sent to your email.', 'success')
                return redirect(url_for('auth.reset_password', email=email))
            flash('If an account with that email exists, a reset link has been sent.', 'success')
            return redirect(url_for('auth.forgot_password'))
        return render_template('forgot_password.html')

    @auth_bp.route('/reset-password', methods=['GET', 'POST'])
    def reset_password():
        from flask import flash, redirect, url_for, request, render_template
        from app.models.User import User
        from app.extensions import db, mail
        from flask_mail import Message
        email = request.args.get('email') or request.form.get('email')
        user = User.query.filter_by(email=email).first() if email else None
        if request.method == 'POST':
            if 'resend_otp' in request.form and user:
                otp = ''.join(random.choices(string.digits, k=6))
                user.otp_code = otp
                user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
                db.session.commit()
                msg = Message('Tourizo Password Reset OTP', recipients=[email])
                msg.body = f"Your Tourizo OTP is: {otp}\nThis code will expire in 10 minutes."
                mail.send(msg)
                flash('A new OTP has been sent to your email.', 'success')
                return render_template('reset_password.html', email=email)
            otp = request.form.get('otp')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            if not user:
                flash('Invalid email address.', 'danger')
                return redirect(url_for('auth.forgot_password'))
            if not otp or not password or not confirm_password:
                flash('All fields are required.', 'danger')
                return render_template('reset_password.html', email=email)
            if user.otp_code != otp or not user.otp_expiry or user.otp_expiry < datetime.utcnow():
                flash('Invalid or expired OTP.', 'danger')
                return render_template('reset_password.html', email=email)
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('reset_password.html', email=email)
            user.set_password(password)
            user.otp_code = None
            user.otp_expiry = None
            db.session.commit()
            flash('Your password has been reset. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        return render_template('reset_password.html', email=email)

register_routes()
