import uuid
from app.pesapal_utils import get_pesapal_token
import requests

from flask import (
    render_template, redirect, url_for, flash,
    request, session, jsonify, current_app
)
from datetime import datetime
from app import db
from app.bookings import bp
from app.bookings.forms import BookingForm, CancelForm, DeleteForm
from app.models.package import Package
from app.models.booking import Booking
from app.email_utils import send_booking_confirmation, send_cancellation_email, send_payment_success_email

PESAPAL_BASE = "https://cybqa.pesapal.com/pesapalv3"



def current_user_id():
    """Get current user ID from session"""
    session.setdefault("user_id", 1)  # Placeholder logic for testing
    return session["user_id"]


def validate_payment_details(method, form_data):
    """Validate payment details based on payment method"""
    errors = []

    if method == 'momo':
        required_fields = ['momo_provider', 'momo_number', 'momo_name']
        for field in required_fields:
            if not form_data.get(field):
                errors.append(f"Mobile Money {field.replace('momo_', '').replace('_', ' ').title()} is required")

        momo_number = form_data.get('momo_number', '')
        if momo_number and (not momo_number.startswith('+256') or len(momo_number) != 13):
            errors.append("Invalid mobile money number format. Use +256XXXXXXXXX")

    elif method == 'card':
        required_fields = ['card_number', 'card_expiry', 'card_cvv', 'card_name']
        for field in required_fields:
            if not form_data.get(field):
                errors.append(f"Card {field.replace('card_', '').replace('_', ' ').title()} is required")

        card_number = form_data.get('card_number', '').replace(' ', '')
        if card_number and (len(card_number) < 13 or len(card_number) > 19):
            errors.append("Invalid card number length")

        card_expiry = form_data.get('card_expiry', '')
        if card_expiry and len(card_expiry) != 5:
            errors.append("Invalid expiry date format. Use MM/YY")

        card_cvv = form_data.get('card_cvv', '')
        if card_cvv and (len(card_cvv) < 3 or len(card_cvv) > 4):
            errors.append("Invalid CVV length")

    elif method == 'bank':
        required_fields = ['bank_name', 'account_number', 'account_name']
        for field in required_fields:
            if not form_data.get(field):
                errors.append(f"Bank {field.replace('_', ' ').title()} is required")

    return errors


def simulate_payment_processing(method, payment_details, amount):
    """Simulate payment processing - replace with actual payment gateway integration"""
    import random
    import time

    time.sleep(1)  # Simulate processing delay

    if random.random() < 0.1:  # 10% failure chance
        return {
            'success': False,
            'error': 'Payment declined by provider',
            'reference': None
        }

    reference = f"{method}_{uuid.uuid4().hex[:10]}"
    return {
        'success': True,
        'reference': reference,
        'amount': amount,
        'method': method
    }


@bp.route("/book", methods=["GET", "POST"])
def book():
    form = BookingForm()
    packages = Package.query.all()
    form.package_id.choices = [(p.id, p.name) for p in packages]
    package_prices = {p.id: float(p.price_per_person) for p in packages}

    if request.method == "GET":
        return render_template("bookings/book.html", form=form, package_prices=package_prices)

    current_app.logger.info(f"=== BOOKING ATTEMPT START ===")
    current_app.logger.info(f"Form data: {dict(request.form)}")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    # Validate form
    if not form.validate_on_submit():
        current_app.logger.error(f"Form validation failed: {form.errors}")
        if is_ajax:
            return jsonify({'success': False, 'message': 'Form validation failed', 'errors': form.errors}), 400
        else:
            for field, errs in form.errors.items():
                for err in errs:
                    flash(f"{field}: {err}", "danger")
            return render_template("bookings/book.html", form=form, package_prices=package_prices)

    # Initialize booking variable
    booking = None
    
    try:
        # Get package
        package = Package.query.get(form.package_id.data)
        if not package:
            raise ValueError(f"Package with ID {form.package_id.data} not found")
        
        current_app.logger.info(f"Package found: {package.name}")
        
        # Calculate total
        total_amount = package.price_per_person * form.num_people.data
        payment_method = form.payment_method.data
        
        current_app.logger.info(f"Total amount: {total_amount}, Payment method: {payment_method}")

        # Validate payment details
        payment_errors = validate_payment_details(payment_method, request.form)
        if payment_errors:
            current_app.logger.error(f"Payment validation failed: {payment_errors}")
            if is_ajax:
                return jsonify({'success': False, 'message': 'Payment validation failed', 'errors': {'payment': payment_errors}}), 400
            else:
                for error in payment_errors:
                    flash(error, "danger")
                return render_template("bookings/book.html", form=form, package_prices=package_prices)

        # Create booking object
        booking = Booking(
            user_id=current_user_id(),
            package_id=package.id,
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            num_people=form.num_people.data,
            total_amount=total_amount,
            booking_date=form.booking_date.data,
            booking_time=form.booking_time.data,
            payment_method=payment_method,
            payment_status='pending'
        )
        
        # Set reference manually (since we removed the default)
        booking.reference = str(uuid.uuid4())
        
        current_app.logger.info(f"Booking object created: {booking.reference}")
        current_app.logger.info(f"Booking details: user_id={booking.user_id}, package_id={booking.package_id}")
        
        # Add to session and flush to get ID
        db.session.add(booking)
        db.session.flush()
        
        current_app.logger.info(f"Booking flushed with ID: {booking.id}")

        # Prepare payment details
        payment_details = {}
        if payment_method == 'momo':
            payment_details = {
                'provider': request.form.get('momo_provider'),
                'number': request.form.get('momo_number'),
                'name': request.form.get('momo_name')
            }
        elif payment_method == 'card':
            payment_details = {
                'number': request.form.get('card_number'),
                'expiry': request.form.get('card_expiry'),
                'cvv': request.form.get('card_cvv'),
                'name': request.form.get('card_name')
            }
        elif payment_method == 'bank':
            payment_details = {
                'bank_name': request.form.get('bank_name'),
                'account_number': request.form.get('account_number'),
                'account_name': request.form.get('account_name')
            }

        current_app.logger.info(f"Processing payment for booking {booking.reference}")
        
        # Process payment
               # Process payment
        if payment_method == 'pesapal':
            db.session.commit()  # Commit the booking before redirecting
            return redirect(url_for("bookings.start_payment", booking_id=booking.id))
        else:
            payment_result = simulate_payment_processing(payment_method, payment_details, total_amount)

        
        current_app.logger.info(f"Payment result: {payment_result}")

        if payment_result['success']:
            current_app.logger.info("Payment successful, updating booking status")
            
            booking.payment_status = 'paid'
            booking.payment_reference = payment_result['reference']

            # Set payment details
            if payment_method == 'momo':
                booking.payment_details = f"Provider: {payment_details['provider']}, Number: ***{payment_details['number'][-4:]}"
            elif payment_method == 'card':
                booking.payment_details = f"Card ending in ***{payment_details['number'][-4:]}"
            elif payment_method == 'bank':
                booking.payment_details = f"Bank: {payment_details['bank_name']}, Account: ***{payment_details['account_number'][-4:]}"

            # Commit the successful booking
            current_app.logger.info("Committing successful booking")
            db.session.commit()
            current_app.logger.info("Successfully committed booking to database")

            # Send emails (after successful commit)
            try:
                send_booking_confirmation(
                    to_email=booking.email,
                    client_name=booking.full_name,
                    booking_reference=booking.reference,
                    total_amount=booking.total_amount,
                    date=booking.booking_date.strftime('%Y-%m-%d'),
                    time=booking.booking_time.strftime('%H:%M')
                )
                send_payment_success_email(
                    to_email=booking.email,
                    client_name=booking.full_name,
                    booking_reference=booking.reference,
                    total_amount=booking.total_amount,
                    payment_method=booking.payment_method,
                   
                    date=booking.booking_date.strftime('%Y-%m-%d'),
                    time=booking.booking_time.strftime('%H:%M')
                )
            except Exception as email_error:
                current_app.logger.warning(f"Email sending failed: {email_error}")
                # Don't fail the booking if email fails

            if is_ajax:
                return jsonify({
                    'success': True,
                    'message': 'Payment successful! Booking confirmed.',
                    'booking_id': booking.id,
                    'payment_reference': booking.payment_reference,
                    'redirect_url': url_for("bookings.list_my_bookings")
                })
            else:
                flash("Payment successful! Booking confirmed.", "success")
                return redirect(url_for("bookings.list_my_bookings"))
        else:
            current_app.logger.info("Payment failed, updating booking status")
            
            booking.payment_status = 'failed'
            
            # Commit the failed booking too (for record keeping)
            current_app.logger.info("Committing failed booking")
            db.session.commit()
            current_app.logger.info("Successfully committed failed booking to database")

            error_message = f"Payment failed: {payment_result['error']}"
            if is_ajax:
                return jsonify({'success': False, 'message': error_message}), 400
            else:
                flash(error_message, "danger")
                return render_template("bookings/book.html", form=form, package_prices=package_prices)

    except Exception as e:
        current_app.logger.error(f"Booking error: {e}", exc_info=True)
        
        # Only rollback if we have an active transaction
        if db.session.is_active:
            db.session.rollback()
            current_app.logger.info("Transaction rolled back due to error")

        if is_ajax:
            return jsonify({'success': False, 'message': 'Booking failed due to system error.', 'error': str(e)}), 500
        else:
            flash("Booking failed. Please try again.", "danger")
            return render_template("bookings/book.html", form=form, package_prices=package_prices)
    
    finally:
        current_app.logger.info("=== BOOKING ATTEMPT END ===")


@bp.route("/my-bookings")
def list_my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user_id()).order_by(Booking.booking_date.desc()).all()
    cancel_form = CancelForm()
    delete_form = DeleteForm()

    return render_template(
        "bookings/my_bookings.html",
        bookings=bookings,
        cancel_form=cancel_form,
        delete_form=delete_form
    )


@bp.route("/edit/<int:booking_id>", methods=["GET", "POST"], endpoint="edit_booking")
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    form = BookingForm(require_payment_method=False, obj=booking)
    packages = Package.query.all()
    form.package_id.choices = [(p.id, p.name) for p in packages]
    package_prices = {p.id: float(p.price_per_person) for p in packages}

    if form.validate_on_submit():
        try:
            package = Package.query.get_or_404(form.package_id.data)
            total_amount = package.price_per_person * form.num_people.data

            booking.full_name = form.full_name.data
            booking.email = form.email.data
            booking.phone = form.phone.data
            booking.num_people = form.num_people.data
            booking.package_id = form.package_id.data
            booking.booking_date = form.booking_date.data
            booking.booking_time = form.booking_time.data
            booking.total_amount = total_amount

            db.session.commit()
            flash("Booking updated successfully.", "success")
            return redirect(url_for("bookings.list_my_bookings"))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Booking update error: {str(e)}")
            flash("Failed to update booking. Please try again.", "danger")

    return render_template("bookings/edit_booking.html", form=form, booking=booking, package_prices=package_prices)


@bp.route("/cancel/<int:booking_id>", methods=["POST"])
def cancel(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user_id():
        flash("Unauthorized access.", "danger")
        return redirect(url_for("bookings.list_my_bookings"))

    try:
        booking.payment_status = 'cancelled'
        db.session.commit()

        try:
            send_cancellation_email(
                to_email=booking.email,
                client_name=booking.full_name,
                booking_reference=booking.reference,
                total_amount=booking.total_amount,
                date=booking.booking_date.strftime('%Y-%m-%d') if booking.booking_date else None,
                time=booking.booking_time.strftime('%H:%M') if booking.booking_time else None
            )
        except Exception as e:
            current_app.logger.warning(f"Cancellation email failed: {str(e)}")

        flash("Booking cancelled successfully.", "info")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Cancellation failed: {str(e)}")
        flash("Could not cancel booking.", "danger")

    return redirect(url_for("bookings.list_my_bookings"))


@bp.route("/delete/<int:booking_id>", methods=["POST"])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user_id():
        flash("Unauthorized access.", "danger")
        return redirect(url_for("bookings.list_my_bookings"))

    if booking.payment_status != 'cancelled':
        flash("Only cancelled bookings can be deleted.", "warning")
        return redirect(url_for("bookings.list_my_bookings"))

    try:
        try:
            send_cancellation_email(
                to_email=booking.email,
                client_name=booking.full_name,
                booking_reference=booking.reference,
                total_amount=booking.total_amount,
                date=booking.booking_date.strftime('%Y-%m-%d') if booking.booking_date else None,
                time=booking.booking_time.strftime('%H:%M') if booking.booking_time else None,
                is_deletion=True
            )
        except Exception as e:
            current_app.logger.warning(f"Deletion email failed: {str(e)}")

        db.session.delete(booking)
        db.session.commit()

        flash("Booking deleted successfully.", "info")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Deletion failed: {str(e)}")
        flash("Could not delete booking.", "danger")

    return redirect(url_for("bookings.list_my_bookings"))


@bp.route("/api/package/<int:package_id>")
def get_package_details(package_id):
    package = Package.query.get_or_404(package_id)
    return jsonify({
        'id': package.id,
        'name': package.name,
        'price_per_person': float(package.price_per_person),
        'description': getattr(package, 'description', ''),
        'duration': getattr(package, 'duration', '')
    })


@bp.route("/pay", methods=["POST"])
def pay():
    booking_id = request.form.get("booking_id")
    method = request.form.get("payment_method")

    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user_id():
        flash("Unauthorized", "danger")
        return redirect(url_for("bookings.list_my_bookings"))

    try:
        reference = f"{method}_token_{uuid.uuid4().hex[:8]}"

        booking.payment_status = "paid"
        booking.payment_method = method
        booking.payment_reference = reference
        db.session.commit()

        send_payment_success_email(
            to_email=booking.email,
            client_name=booking.full_name,
            booking_reference=booking.reference,
            total_amount=booking.total_amount,
            payment_method=booking.payment_method,
            date=booking.booking_date.strftime('%Y-%m-%d') if booking.booking_date else None,
            time=booking.booking_time.strftime('%H:%M') if booking.booking_time else None
        )

        flash("Payment successful!", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Payment error: {str(e)}")
        flash("Payment failed.", "danger")

    return redirect(url_for("bookings.list_my_bookings"))


@bp.route("/api/check-availability", methods=["POST"])
def check_availability():
    data = request.get_json()
    package_id = data.get('package_id')
    booking_date = data.get('booking_date')

    if not package_id or not booking_date:
        return jsonify({'available': False, 'message': 'Missing required data'}), 400

    try:
        check_date = datetime.strptime(booking_date, '%Y-%m-%d').date()

        package = Package.query.get(package_id)
        if not package:
            return jsonify({'available': False, 'message': 'Package not found'}), 404

        existing_bookings = Booking.query.filter_by(
            package_id=package_id,
            booking_date=check_date
        ).filter(
            Booking.payment_status != 'cancelled'
        ).count()

        max_bookings = getattr(package, 'max_daily_bookings', 10)
        available = existing_bookings < max_bookings

        return jsonify({
            'available': available,
            'existing_bookings': existing_bookings,
            'max_bookings': max_bookings,
            'message': 'Available' if available else 'Fully booked for this date'
        })

    except ValueError:
        return jsonify({'available': False, 'message': 'Invalid date format'}), 400
    except Exception as e:
        current_app.logger.error(f"Availability check error: {str(e)}")
        return jsonify({'available': False, 'message': 'Error checking availability'}), 500
    
    from app.pesapal_utils import get_pesapal_token

@bp.route("/start-payment/<int:booking_id>")
def start_payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    try:
        ipn_id = "your_saved_ipn_id_here"  # Use the one returned from register_ipn_url()

        token = get_pesapal_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "id": str(uuid.uuid4()),
            "currency": "UGX",
            "amount": booking.total_amount,
            "description": f"Booking payment for {booking.full_name}",
            "callback_url": "https://your-public-ngrok-url/webhook/pesapal",
            "notification_id": ipn_id,
            "billing_address": {
                "email_address": booking.email,
                "phone_number": booking.phone,
                "first_name": booking.full_name.split()[0],
                "last_name": booking.full_name.split()[-1],
            }
        }

        res = requests.post(
            f"{PESAPAL_BASE}/api/Transactions/SubmitOrderRequest",
            headers=headers,
            json=payload
        )
        data = res.json()

        booking.reference = data["merchant_reference"]
        booking.payment_status = "pending"
        db.session.commit()

        return redirect(data["redirect_url"])

    except Exception as e:
        current_app.logger.error(f"PesaPal order error: {e}")
        flash("Could not start payment.", "danger")
        return redirect(url_for("bookings.list_my_bookings"))
@bp.route("/webhook/pesapal", methods=["POST"])
def pesapal_webhook():
    data = request.get_json()
    tracking_id = data.get("order_tracking_id")
    merchant_reference = data.get("merchant_reference")

    token = get_pesapal_token()
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(
        f"{PESAPAL_BASE}/api/Transactions/GetTransactionStatus",
        headers=headers,
        params={"orderTrackingId": tracking_id}
    )

    status_data = res.json()
    status = status_data.get("payment_status")

    booking = Booking.query.filter_by(reference=merchant_reference).first()
    if booking:
        booking.payment_status = status.lower()
        db.session.commit()

    return {"message": "Status updated"}, 200

