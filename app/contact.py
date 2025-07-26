from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_mail import Message
from app.extensions import mail
import logging
import traceback
from datetime import datetime
from app.forms import ContactForm
from app.models.Inquiry import Inquiry
contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        try:
            # Get form data - match the HTML form field names
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            contact_method = request.form.get('contact_method', '').strip()
            group_size = request.form.get('group_size', '1').strip()
            country = request.form.get('country', '').strip()
            message = request.form.get('message', '').strip()
            heard_about = request.form.getlist('heard_about')
            
            # Debug: Print form data
            print(f"DEBUG: Form data received:")
            print(f"  Name: {first_name} {last_name}")
            print(f"  Email: {email}")
            print(f"  Phone: {phone}")
            print(f"  Contact method: {contact_method}")
            
            # Validate required fields
            if not all([first_name, last_name, email, phone, contact_method, country]):
                missing_fields = []
                if not first_name: missing_fields.append("first_name")
                if not last_name: missing_fields.append("last_name")
                if not email: missing_fields.append("email")
                if not phone: missing_fields.append("phone")
                if not contact_method: missing_fields.append("contact_method")
                if not country: missing_fields.append("country")
                
                print(f"DEBUG: Missing required fields: {missing_fields}")
                flash(f"Please fill in all required fields: {', '.join(missing_fields)}", "danger")
                return redirect(url_for('contact.contact_form'))
            
            # Debug: Print mail configuration
            print(f"DEBUG: Mail configuration:")
            print(f"  MAIL_SERVER: {current_app.config.get('MAIL_SERVER')}")
            print(f"  MAIL_PORT: {current_app.config.get('MAIL_PORT')}")
            print(f"  MAIL_USE_TLS: {current_app.config.get('MAIL_USE_TLS')}")
            print(f"  MAIL_USERNAME: {current_app.config.get('MAIL_USERNAME')}")
            print(f"  MAIL_PASSWORD: {'*' * len(str(current_app.config.get('MAIL_PASSWORD', '')))}")
            print(f"  MAIL_DEFAULT_SENDER: {current_app.config.get('MAIL_DEFAULT_SENDER')}")
            
            # Get admin email from config
            admin_email = current_app.config.get('ADMIN_EMAIL', 'ssekiziyivugrace55@gmail.com')
            print(f"DEBUG: Admin email: {admin_email}")
            
            # Compose email with better formatting
            email_body = f"""
New Contact Form Submission from TOURIZO Website

CUSTOMER DETAILS:
==================
Name: {first_name} {last_name}
Email: {email}
Phone: {phone}
Preferred Contact Method: {contact_method}
Group Size: {group_size}
Country/Region: {country}

HOW THEY HEARD ABOUT US:
========================
{', '.join(heard_about) if heard_about else 'Not specified'}

MESSAGE:
========
{message if message else 'No message provided'}

SUBMISSION TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """.strip()
            
            print(f"DEBUG: Creating email message...")
            
            # Create email message
            msg = Message(
                subject=f"New Contact Inquiry from {first_name} {last_name}",
                recipients=[admin_email],
                body=email_body,
                reply_to=email
            )
            
            print(f"DEBUG: Message created, attempting to send...")
            
            # Send email with error handling
            mail.send(msg)
            
            print(f"DEBUG: Email sent successfully!")
            current_app.logger.info(f"Contact form email sent successfully to {admin_email}")
            flash("Your message has been sent successfully! We'll get back to you soon.", "success")
            
        except Exception as e:
            # Print detailed error information
            print(f"ERROR: Email sending failed!")
            print(f"ERROR: Exception type: {type(e).__name__}")
            print(f"ERROR: Exception message: {str(e)}")
            print(f"ERROR: Full traceback:")
            print(traceback.format_exc())
            
            # Log the detailed error
            current_app.logger.error(f"Email sending error: {str(e)}")
            current_app.logger.error(f"Full traceback: {traceback.format_exc()}")
            
            # Show specific error to user (for debugging - remove in production)
            flash(f"Email error: {str(e)}", "danger")
            
        return redirect(url_for('auth.user_dashboard'))

    return render_template('contact.html')


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
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_mail import Message
from flask_login import login_required, current_user
from app.extensions import mail, db


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

    return render_template('contact_form.html', form=form)
