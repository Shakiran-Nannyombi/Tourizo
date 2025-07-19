from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from forms import UserProfileForm
from models import Inquiry, User, db, Tour, Booking
from extensions import mail  # Import mail from extensions
from app.decorators import admin_required
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_admin = request.form.get('admin') == 'true'

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email, is_admin=is_admin)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('auth.admin_dashboard'))
        else:
            return redirect(url_for('auth.user_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')

            if user.is_admin:
                return redirect(url_for('auth.admin_dashboard'))
            else:
                return redirect(url_for('auth.user_dashboard'))

        flash('Invalid email or password.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    form = UserProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Profile updated successfully!', 'success')

        # ✅ Redirect to user dashboard after update
        return redirect(url_for('auth.user_dashboard'))

    return render_template('profile.html', form=form)


@auth.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/user/dashboard')
@login_required
def user_dashboard():
    username = current_user.username
    user_bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    return render_template('user_dashboard.html', username=username, bookings=user_bookings)

@auth.route("/submit_contact", methods=["POST"])
def submit_contact():
    subject = request.form.get("subject")
    message = request.form.get("message")
    user_id = current_user.id if current_user.is_authenticated else None

    # Save to database
    inquiry = Inquiry(subject=subject, message=message, user_id=user_id)
    db.session.add(inquiry)
    db.session.commit()

    # Send email
    msg = Message(subject=subject,
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[current_app.config['ADMIN_EMAIL']],
                  body=message)
    mail.send(msg)

    flash("Message sent successfully!", "success")
    return redirect(url_for("auth.user_dashboard"))
@auth.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    total_tours = Tour.query.count()
    total_bookings = Booking.query.count()
    total_users = User.query.count()
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
    draft_tours = Tour.query.filter_by(is_active=False).count()

    return render_template('admin/dashboard.html', 
                           total_tours=total_tours,
                           total_bookings=total_bookings,
                           total_users=total_users,
                           recent_bookings=recent_bookings,
                           draft_tours=draft_tours,
                           current_time=datetime.utcnow())