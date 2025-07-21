# Tourizo: Tour and Travels Web App

## Project Overview
Tourizo is a web application for managing tour packages, bookings, reviews, and admin analytics. Built with Flask, it is structured for collaborative development with clear separation of concerns using Blueprints and models.

## Project Structure
```
Tourizo/
│
├── app/
│   ├── __init__.py
│   ├── admin.py
│   ├── auth.py
│   ├── bookings.py
│   ├── config.py
│   ├── decorators.py
│   ├── email_service.py
│   ├── email_utils.py
│   ├── extensions.py
│   ├── filters.py
│   ├── forms.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── Booking.py
│   │   ├── Category.py
│   │   ├── Destination.py
│   │   ├── Inquiry.py
│   │   ├── Review.py
│   │   ├── Tour.py
│   │   ├── TourDate.py
│   │   ├── TourPackage.py
│   │   └── User.py
│   ├── pesapal_utils.py
│   ├── reviews.py
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   │   └── tours/
│   │   ├── js/
│   ├── templates/
│   │   ├── admin/
│   │   │   ├── add_tour.html
│   │   │   ├── dashboard.html
│   │   │   ├── edit_tour.html
│   │   │   └── manage_tours.html
│   │   ├── base.html
│   │   ├── bookings/
│   │   │   ├── book.html
│   │   │   ├── cancel_booking.html
│   │   │   ├── edit_booking.html
│   │   │   └── my_bookings.html
│   │   ├── errors/
│   │   │   ├── 401.html
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   ├── login.html
│   │   ├── partials/
│   │   │   └── tour_card.html
│   │   ├── register.html
│   │   ├── reviews/
│   │   │   └── add_review.html
│   │   ├── tour_detail.html
│   │   ├── tours.html
│   │   ├── user_dashboard.html
│   │   └── welcome.html
│   ├── tours.py
│   └── utils.py
│
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       ├── 0a45b1eab94f_add_booking_date_and_booking_time_to_.py
│       ├── 144b19ab5fde_merge_migration_branches.py
│       ├── 14636034cefc_add_destination_column_to_tour.py
│       ├── 1b4fa2c39468_add_order_tracking_id_to_booking.py
│       ├── 33e4476f651f_updated_booking_model.py
│       ├── 4c0e23c19a5c_add_cancellation_tracking_fields.py
│       ├── 531ed7a66213_add_short_description_to_tour.py
│       ├── 6603467eefea_add_payment_fields.py
│       ├── 67305048430e_add_payment_fields_to_booking.py
│       ├── 6b62d392a450_add_destination_id_to_tour.py
│       ├── 77ce3642259e_create_tour_model.py
│       ├── 798c2116a4d4_add_payment_fields_to_booking.py
│       ├── 83b0250f1a0f_add_bookings_table.py
│       ├── e04a9e556ef0_create_packages_table.py
│       ├── f92f5d48952a_add_reviews_relationship.py
│
├── requirements.txt
├── run.py
└── README.md
```

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Tourizo
   ```
2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the app:**
   ```bash
   python run.py
   ```
   The app will be available at `http://127.0.0.1:5000/`.

## Team Breakdown & Responsibilities

### 👤 Member 1: User Authentication & Profile Management
- **Files:** `auth.py`, `models/User.py`, templates/auth/
- **Features:** Registration, login/logout, profile updates, password hashing, input validation, role-based access, session handling

### 👤 Member 2: Tour Packages Management
- **Files:** `tours.py`, `models/TourPackage.py`, templates/tours/
- **Features:** CRUD for tours, search/filter, admin interface, forms

### 👤 Member 3: Booking System & Payments
- **Files:** `bookings.py`, `models/Booking.py`, templates/bookings/
- **Features:** Booking creation, confirmation, payment simulation, email notifications, booking history

### 👤 Member 4: Admin Dashboard, Reports, Inquiries
- **Files:** `admin.py`, `models/Inquiry.py`, templates/admin/
- **Features:** Contact form, admin dashboard, analytics (Chart.js), logging, blueprints structure

### 👤 Member 5: Reviews, Frontend UI/UX, Deployment
- **Files:** `reviews.py`, `models/Review.py`, templates/reviews/
- **Features:** Reviews/ratings, responsive UI, deployment setup, HTML/CSS/JS consistency

## Notes
- All models use SQLAlchemy (see `app/models/`).
- Blueprints are registered in `app/__init__.py`.
- Use `base.html` for template inheritance.
- Update `config.py` for production settings (e.g., secret key, database URI).
- For email, configure Flask-Mail in `config.py` and `email_service.py`.

---
Happy coding! 🚀
