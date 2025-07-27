from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_mail import Message
from flask_login import login_required, current_user
from app.extensions import mail, db
import logging
import traceback
from datetime import datetime
from app.models.Inquiry import Inquiry
from app.forms import ContactForm

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['GET', 'POST'])
@login_required
def contact_form():
    form = ContactForm()

    if form.validate_on_submit():
        # Save inquiry
        inquiry = Inquiry(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(inquiry)
        db.session.commit()

        # Send email to admin
        admin_email = current_app.config.get('ADMIN_EMAIL', 'ssekiziyivugrace55@gmail.com')
        msg = Message(subject="New Inquiry from Tourizo",
                      sender=form.email.data,
                      recipients=[admin_email],
                      body=f"Name: {form.name.data}\nEmail: {form.email.data}\n\nMessage:\n{form.message.data}")
        mail.send(msg)

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for('auth.user_dashboard'))  # Or whichever dashboard route you use

    return render_template('contact.html', form=form)

@contact_bp.route('/faq')
def faq():
    return render_template('faq.html')

@contact_bp.route('/inquiries')
@login_required
def my_inquiries():
    inquiries = Inquiry.query.filter_by(user_id=current_user.id).order_by(Inquiry.timestamp.desc()).all()
    return render_template('inquiries.html', inquiries=inquiries)


# Simple test email function
@contact_bp.route('/test-email')
def test_email():
    try:
        print("DEBUG: Testing email configuration...")
        
        # Print all mail configuration
        print(f"MAIL_SERVER: {current_app.config.get('MAIL_SERVER')}")
        print(f"MAIL_PORT: {current_app.config.get('MAIL_PORT')}")
        print(f"MAIL_USE_TLS: {current_app.config.get('MAIL_USE_TLS')}")
        print(f"MAIL_USERNAME: {current_app.config.get('MAIL_USERNAME')}")
        print(f"MAIL_PASSWORD configured: {bool(current_app.config.get('MAIL_PASSWORD'))}")
        
        admin_email = current_app.config.get('ADMIN_EMAIL', 'ssekiziyivugrace55@gmail.com')
        print(f"Admin email: {admin_email}")
        
        msg = Message(
            subject="Test Email from Travel App",
            recipients=[admin_email],
            body="This is a test email to verify email configuration is working."
        )
        
        print("Attempting to send test email...")
        mail.send(msg)
        print("Test email sent successfully!")
        
        return f"Test email sent successfully to {admin_email}"
        
    except Exception as e:
        print(f"Test email failed: {str(e)}")
        print(f"Full traceback:")
        print(traceback.format_exc())
        current_app.logger.error(f"Test email failed: {str(e)}")
        return f"Test email failed: {str(e)}", 500


# Check mail configuration endpoint
@contact_bp.route('/check-config')
def check_config():
    """Endpoint to check current mail configuration"""
    config_info = {
        'MAIL_SERVER': current_app.config.get('MAIL_SERVER'),
        'MAIL_PORT': current_app.config.get('MAIL_PORT'),
        'MAIL_USE_TLS': current_app.config.get('MAIL_USE_TLS'),
        'MAIL_USERNAME': current_app.config.get('MAIL_USERNAME'),
        'MAIL_PASSWORD_SET': bool(current_app.config.get('MAIL_PASSWORD')),
        'MAIL_DEFAULT_SENDER': current_app.config.get('MAIL_DEFAULT_SENDER'),
        'ADMIN_EMAIL': current_app.config.get('ADMIN_EMAIL')
    }
    
    return f"<pre>{str(config_info)}</pre>"
