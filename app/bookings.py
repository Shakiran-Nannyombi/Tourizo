from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from app.models.Booking import Booking
from app.models.Tour import Tour
from app.utils import generate_booking_reference
from app.forms import BookingForm, CancelForm, DeleteForm, PaymentForm
from app.email_utils import send_cancellation_email, send_payment_success_email
from app.extensions import db

bookings_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

def register_routes():
    @bookings_bp.route('/book', defaults={'tour_id': None}, methods=['GET', 'POST'])
    @bookings_bp.route('/book/<int:tour_id>', methods=['GET', 'POST'])
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
                return redirect(url_for('bookings.book'))

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
                    payment_status='paid',  #  Mark as paid immediately
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

                flash("Booking successful!", "info")
                return redirect(url_for('user_dashboard'))

            except Exception as e:
                db.session.rollback()
                print(f"Booking error: {e}")
                flash('An error occurred. Please try again.', 'error')

        elif request.method == 'POST':
            print("Form validation errors:", form.errors)
            flash("Please correct the errors in the form.", "warning")

        return render_template('bookings/book.html', form=form, tour_prices=tour_prices)

    @bookings_bp.route("/my-bookings")
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

    @bookings_bp.route('/edit/<int:booking_id>', methods=['GET', 'POST'])
    @login_required
    def edit_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)
        
        # Check that the current user owns this booking or is admin
        if booking.user_id != current_user.id and not getattr(current_user, 'is_admin', False):
            abort(403)
        
        # Get all tours for the form choices
        tours = Tour.query.all()
        form = BookingForm()
        form.tour_id.choices = [(tour.id, tour.title) for tour in tours]
        
        if form.validate_on_submit():
            # Update booking with form data
            selected_tour = Tour.query.get(form.tour_id.data)
            if not selected_tour:
                flash('Selected tour not found.', 'error')
                return redirect(url_for('bookings.edit_booking', booking_id=booking_id))
            
            try:
                # Update booking fields
                booking.full_name = form.full_name.data
                booking.email = form.email.data
                booking.phone = form.phone.data
                booking.booking_date = form.booking_date.data
                booking.booking_time = form.booking_time.data
                booking.num_people = form.num_people.data
                booking.total_amount = float(selected_tour.price) * form.num_people.data
                booking.tour_id = selected_tour.id
                if hasattr(form, 'special_requests'):
                    booking.special_requests = form.special_requests.data
                
                db.session.commit()
                flash('Booking updated successfully!', 'success')
                return redirect(url_for('bookings.my_bookings'))
                
            except Exception as e:
                db.session.rollback()
                print(f"Booking update error: {e}")
                flash('An error occurred while updating the booking. Please try again.', 'error')
        
        elif request.method == 'GET':
            # Pre-populate form with existing booking data
            form.full_name.data = booking.full_name
            form.email.data = booking.email
            form.phone.data = booking.phone
            form.booking_date.data = booking.booking_date
            form.booking_time.data = booking.booking_time
            form.num_people.data = booking.num_people
            form.tour_id.data = booking.tour_id
            if hasattr(form, 'special_requests') and booking.special_requests:
                form.special_requests.data = booking.special_requests
        
        elif request.method == 'POST':
            print("Form validation errors:", form.errors)
            flash("Please correct the errors in the form.", "warning")
        
        return render_template('bookings/edit_booking.html', form=form, booking=booking)

    @bookings_bp.route('/cancel-booking/<int:booking_id>', methods=['GET', 'POST'])
    def cancel_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)
        form = CancelForm()

        if form.validate_on_submit():
            reason = form.reason.data
            notes = form.notes.data

            try:
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
                return redirect(url_for('bookings.my_bookings'))

            except Exception as e:
                db.session.rollback()
                print(f"Cancellation error: {e}")
                flash('An error occurred while cancelling the booking. Please try again.', 'error')

        return render_template('bookings/cancel_booking.html', booking=booking, form=form)

    @bookings_bp.route('/delete-booking/<int:booking_id>', methods=['POST'])
    @login_required
    def delete_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)

        # Check that the current user is the owner of the booking or is admin
        if booking.user_id != current_user.id and not getattr(current_user, 'is_admin', False):
            abort(403)
        
        try:
            # Optional: Send deletion notification email
            try:
                send_cancellation_email(
                    to_email=booking.email,
                    client_name=booking.full_name,
                    booking_reference=booking.reference,
                    total_amount=booking.total_amount,
                    reason="Booking deleted by user",
                    notes="This booking has been permanently deleted.",
                    date=str(booking.booking_date),
                    time=str(booking.booking_time),
                    is_deletion=True
                )
            except Exception as email_error:
                print(f"Email notification error during deletion: {email_error}")
                # Continue with deletion even if email fails
            
            # Actually delete the booking from database
            db.session.delete(booking)
            db.session.commit()
            
            flash('Booking deleted successfully.', 'success')
            
        except Exception as e:
            db.session.rollback()
            print(f"Booking deletion error: {e}")
            flash('An error occurred while deleting the booking. Please try again.', 'error')
        
        return redirect(url_for('bookings.my_bookings'))

    @bookings_bp.route('/pay', methods=['POST'])
    @login_required
    def pay():
        # Placeholder: handle payment logic here
        booking_id = request.form.get('booking_id')
        
        if booking_id:
            try:
                booking = Booking.query.get_or_404(booking_id)
                
                # Check that the current user owns this booking
                if booking.user_id != current_user.id and not getattr(current_user, 'is_admin', False):
                    abort(403)
                
                # Update payment status
                booking.payment_status = 'paid'
                db.session.commit()
                
                # Send payment confirmation email
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
                except Exception as email_error:
                    print(f"Payment email error: {email_error}")
                
                flash(f'Payment received for booking {booking.reference}!', 'success')
                
            except Exception as e:
                db.session.rollback()
                print(f"Payment error: {e}")
                flash('An error occurred while processing payment. Please try again.', 'error')
        else:
            flash('Invalid booking ID.', 'error')
        
        return redirect(url_for('bookings.my_bookings'))

register_routes()