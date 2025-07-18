from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.models.Tour import Tour
from app.models.Category import Category
from app.models.Destination import Destination
from app.models.Review import Review
from app.models.TourDate import TourDate
from app.forms import TourSearchForm
import json
from app.utils import generate_booking_reference

tours_bp = Blueprint('tours', __name__, url_prefix='/tours')

def register_routes():
    @tours_bp.route('/', methods=['GET'])
    def list_tours():
        form = TourSearchForm()
        search = request.args.get('search', '')
        destination = request.args.get('destination', '')
        category_id = request.args.get('category', type=int)
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        page = request.args.get('page', 1, type=int)

        query = Tour.query.filter_by(is_active=True)
        if search:
            query = query.filter(Tour.title.contains(search) | Tour.description.contains(search))
        if destination:
            query = query.filter(Tour.destination.contains(destination))
        if category_id and category_id != 0:
            query = query.filter_by(category_id=category_id)
        if min_price:
            query = query.filter(Tour.price >= min_price)
        if max_price:
            query = query.filter(Tour.price <= max_price)

        tours = query.paginate(page=page, per_page=10, error_out=False)
        categories = Category.query.all()
        destinations = Destination.query.all()
        form.category.choices = [(0, 'All Categories')] + [(c.id, c.name) for c in categories]

        return render_template('tours.html', tours=tours, form=form, categories=categories, destinations=destinations, filters={
            'search': search,
            'destination': destination,
            'category': category_id,
            'min_price': min_price,
            'max_price': max_price
        })

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
        return render_template('tour_detail.html', tour=tour, image_list=image_list, related_tours=related_tours, reviews=reviews, available_dates=available_dates)

register_routes()
