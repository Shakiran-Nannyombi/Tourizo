from flask import Blueprint

tours_bp = Blueprint('tours', __name__, url_prefix='/tours')

# Placeholder routes
def register_routes():
    @tours_bp.route('/')
    def list_tours():
        return 'List Tours (to be implemented)'

    @tours_bp.route('/<int:tour_id>')
    def tour_detail(tour_id):
        return f'Tour Detail {tour_id} (to be implemented)'

register_routes()
