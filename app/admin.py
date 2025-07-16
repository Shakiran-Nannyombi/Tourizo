from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.Inquiry import Inquiry
from app import db
import logging

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../templates/admin')

logging.basicConfig(filename='admin.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@admin_bp.route('/dashboard')
def dashboard():
    from sqlalchemy import func
    inquiries_count = Inquiry.query.count()
    return render_template('dashboard.html', inquiries_count=inquiries_count)

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
