from flask import Blueprint

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

# Placeholder routes
def register_routes():
    @reviews_bp.route('/')
    def list_reviews():
        return 'List Reviews (to be implemented)'

    @reviews_bp.route('/add')
    def add_review():
        return 'Add Review (to be implemented)'

register_routes()
