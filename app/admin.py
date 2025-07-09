from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Placeholder routes
def register_routes():
    @admin_bp.route('/')
    def dashboard():
        return 'Admin Dashboard (to be implemented)'

    @admin_bp.route('/inquiries')
    def inquiries():
        return 'Inquiries (to be implemented)'

register_routes()
