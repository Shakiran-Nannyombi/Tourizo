# app/email_utils.py
from flask import current_app
from flask_mail import Message
from app.extensions import mail
#from main import mail


# ----------------------------------------------------------------------
# Helper to build the schedule string once
# ----------------------------------------------------------------------
def _format_schedule(date_str: str | None, time_str: str | None) -> str:
    """
    Return a nicely‑formatted schedule string – or "" if nothing supplied.
    """
    parts = []
    if date_str:
        parts.append(f"Date: {date_str}")
    if time_str:
        parts.append(f"Time: {time_str}")
    return "\n".join(parts) if parts else ""


# ----------------------------------------------------------------------
# Booking confirmation
# ----------------------------------------------------------------------
def send_booking_confirmation(to_email, client_name,
                              booking_reference, total_amount,
                              date=None, time=None):
    """
    Send booking confirmation. `date` / `time` are optional strings.
    """
    when_block = _format_schedule(date, time)          # <- use helper
    when_line = f"\n{when_block}" if when_block else ""
    body = (
    f"Hello {client_name},\n\n"
    "Thank you for booking with us!\n\n"
    f"Booking Reference: {booking_reference}\n"
    f"Total Amount Paid: {total_amount:,.0f} UGX{when_line}\n\n"
    "We look forward to hosting you.\n\n"
    "Regards,\nThe Tour Team – TravelMate Tours"
)
    try:
        msg = Message(
            subject="Your Booking Confirmation",
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
            recipients=[to_email],
            body=body
        )
        mail.send(msg)
        current_app.logger.info("Booking confirmation sent to %s", to_email)
        return True
    except Exception as e:
        current_app.logger.error("Failed to send booking confirmation: %s", e)
        return False


# ----------------------------------------------------------------------
# Cancellation
# ----------------------------------------------------------------------
def send_cancellation_email(to_email, client_name, booking_reference,
                            total_amount, reason=None, notes=None,
                            date=None, time=None, is_deletion=False):

    when_block = _format_schedule(date, time)
    schedule_text = f" scheduled for {date} at {time}" if when_block else ""

    if is_deletion:
        subject = f"Booking Deleted: {booking_reference}"
        intro   = "has been permanently deleted"
    else:
        subject = f"Booking Cancelled: {booking_reference}"
        intro   = "has been cancelled"

    # ── HTML ───────────────────────────────────────────────
    html = f"""
        <h2>Booking { 'Deletion' if is_deletion else 'Cancellation' } Confirmation</h2>
        <p>Dear {client_name},</p>
        <p>Your booking (Reference: <strong>{booking_reference}</strong>){schedule_text} {intro}.</p>
        <p><strong>Amount:</strong> {total_amount:,.0f} UGX</p>
        {f"<p><strong>Reason:</strong> {reason}</p>" if reason else ""}
        {f"<p><strong>Notes:</strong> {notes}</p>" if notes else ""}
        <p>Regards,<br>TravelMate Tours</p>
    """

    # ── Plain text ─────────────────────────────────────────
    text = (
        f"Hi {client_name},\n\n"
        f"Your booking {booking_reference}{schedule_text} {intro}.\n"
        f"Amount: {total_amount:,.0f} UGX\n"
        f"{'Reason: ' + reason if reason else ''}\n"
        f"{'Notes: ' + notes  if notes  else ''}\n\n"
        "Regards,\nTravelMate Tours"
    )

    try:
        msg = Message(subject=subject,
                      sender=current_app.config["MAIL_DEFAULT_SENDER"],
                      recipients=[to_email],
                      body=text,
                      html=html)
        mail.send(msg)
        current_app.logger.info("Cancellation e‑mail sent to %s", to_email)
        return True
    except Exception as e:
        current_app.logger.error("Failed to send cancellation e‑mail: %s", e)
        return False
# ----------------------------------------------------------------------
# Payment successful email
# ----------------------------------------------------------------------
def send_payment_success_email(to_email, client_name, booking_reference,
                               total_amount, payment_method=None, payment_reference=None,
                               date=None, time=None):
    """
    Send email confirming that payment was received.
    """
    when_block = _format_schedule(date, time)

    method_str = f" via {payment_method.capitalize()}" if payment_method else ""

    # ── Plain Text ──
    text = (
        f"Hello {client_name},\n\n"
        f"We've received your payment{method_str} for your booking.\n\n"
        f"Booking Reference: {booking_reference}\n"
        f"Payment Reference: {payment_reference}\n"
        f"Amount Paid: {total_amount:,.0f} UGX\n"
        f"{when_block}\n\n"
        "Thank you for booking with TravelMate Tours.\n\n"
        "Warm regards,\nTravelMate Tours"
    )

    # ── HTML ──
    html = f"""
        <h2>Payment Received</h2>
        <p>Dear {client_name},</p>
        <p>Your payment{method_str} has been received for the booking below:</p>
        <ul>
            <li><strong>Booking Reference:</strong> {booking_reference}</li>
            <li><strong>Amount Paid:</strong> {total_amount:,.0f} UGX</li>
            {f"<li><strong>Date:</strong> {date}</li>" if date else ""}
            {f"<li><strong>Time:</strong> {time}</li>" if time else ""}
        </ul>
        <p>Thank you for choosing TravelMate Tours.</p>
        <p>Warm regards,<br><strong>TravelMate Tours</strong></p>
    """

    try:
        msg = Message(
            subject="Payment Confirmation – TravelMate Tours",
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
            recipients=[to_email],
            body=text,
            html=html
        )
        mail.send(msg)
        current_app.logger.info("Payment email sent to %s", to_email)
        return True
    except Exception as e:
        current_app.logger.error("Failed to send payment email: %s", e)
        return False