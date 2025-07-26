from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.models.Tour import Tour
from app.models.Category import Category
from app.models.Destination import Destination
from app.models.Review import Review
from app.models.TourDate import TourDate
from app.forms import TourSearchForm
import json
from app.utils import generate_booking_reference
from flask_login import login_required, current_user

tours_bp = Blueprint('tours', __name__, url_prefix='/tours')

def register_routes():
    @tours_bp.route('/', methods=['GET'])
    def list_tours():
        search = request.args.get('search', '')
        category_id = request.args.get('category', type=int)
        duration = request.args.get('duration', '')
        page = request.args.get('page', 1, type=int)

        query = Tour.query.filter_by(is_active=True)
        
        # Search filter
        if search:
            query = query.filter(Tour.title.contains(search) | Tour.description.contains(search))
        
        # Category filter
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        # Duration filter
        if duration:
            if duration == '1-3':
                query = query.filter(Tour.duration.between(1, 3))
            elif duration == '4-7':
                query = query.filter(Tour.duration.between(4, 7))
            elif duration == '8+':
                query = query.filter(Tour.duration >= 8)

        # Order by creation date (newest first)
        query = query.order_by(Tour.created_at.desc())
        
        tours = query.paginate(page=page, per_page=12, error_out=False)
        categories = Category.query.all()
        wishlist_ids = set()
        if current_user.is_authenticated:
            wishlist_ids = set(t.id for t in getattr(current_user, 'wishlist', []))
        return render_template('tours.html', tours=tours, categories=categories, wishlist_ids=wishlist_ids)

    @tours_bp.route('/<int:tour_id>', methods=['GET'])
    def tour_detail(tour_id):
        tour = Tour.query.get_or_404(tour_id)
        image_list = []
        if tour.image_gallery:
            try:
                image_list = json.loads(tour.image_gallery)
            except Exception as e:
                print("Gallery parse error:", e)
        related_tours = Tour.query.filter(Tour.category_id == tour.category_id, Tour.id != tour.id).limit(4).all()
        reviews = Review.query.filter_by(tour_id=tour_id, is_approved=True).all()
        available_dates = TourDate.query.filter_by(tour_id=tour_id, is_available=True).all()
        wishlist_ids = set()
        if current_user.is_authenticated:
            wishlist_ids = set(t.id for t in getattr(current_user, 'wishlist', []))
        return render_template('tour_detail.html', tour=tour, image_list=image_list, related_tours=related_tours, reviews=reviews, available_dates=available_dates, itinerary_days=tour.itinerary_days, wishlist_ids=wishlist_ids)

    @tours_bp.route('/wishlist', methods=['GET'])
    @login_required
    def wishlist():
        wishlist_tours = current_user.wishlist
        wishlist_ids = set(t.id for t in getattr(current_user, 'wishlist', []))
        return render_template('wishlist.html', tours=wishlist_tours, wishlist_ids=wishlist_ids)

    @tours_bp.route('/wishlist/add/<int:tour_id>', methods=['POST'])
    @login_required
    def add_to_wishlist(tour_id):
        tour = Tour.query.get_or_404(tour_id)
        if tour not in current_user.wishlist:
            current_user.wishlist.append(tour)
            from app.extensions import db
            db.session.commit()
        return {'success': True, 'count': len(current_user.wishlist)}

    @tours_bp.route('/wishlist/remove/<int:tour_id>', methods=['POST'])
    @login_required
    def remove_from_wishlist(tour_id):
        tour = Tour.query.get_or_404(tour_id)
        if tour in current_user.wishlist:
            current_user.wishlist.remove(tour)
            from app.extensions import db
            db.session.commit()
        return {'success': True, 'count': len(current_user.wishlist)}

    @tours_bp.route('/wishlist/count', methods=['GET'])
    @login_required
    def wishlist_count():
        return {'count': len(current_user.wishlist)}

register_routes()
