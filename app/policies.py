from flask import Blueprint, render_template

policies_bp = Blueprint('policies', __name__, url_prefix='/policies')

@policies_bp.route('/booking-policy')
def booking_policy():
    return render_template('policies/booking_policy.html')

@policies_bp.route('/cancellation')
def cancellation():
    return render_template('policies/cancellation.html')

@policies_bp.route('/terms-conditions')
def terms_conditions():
    return render_template('policies/terms_conditions.html')

@policies_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('policies/privacy_policy.html') 