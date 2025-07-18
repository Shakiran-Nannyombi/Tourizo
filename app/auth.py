from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.User import User
from app.extensions import db
from functools import wraps
from flask import make_response

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
        return render_template('user_dashboard.html')

    @auth_bp.route('/logout')
    @login_required
    def logout():
        logout_user()
        session.clear()  # Clear all session data for extra security
        flash('You have been logged out.', 'info')
        return redirect(url_for('welcome'))

register_routes()
