# Tourizo: Tour and Travels Web App

## Project Overview
Tourizo is a web application for managing tour packages, bookings, reviews, and admin analytics. Built with Flask, it is structured for collaborative development with clear separation of concerns using Blueprints and models.

## Project Structure
```
Tourizo/
│
├── app/
│   ├── __init__.py         # Flask app factory, blueprint registration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── User.py
│   │   ├── TourPackage.py
│   │   ├── Booking.py
│   │   ├── Inquiry.py
│   │   └── Review.py
│   ├── auth.py             # User authentication blueprint
│   ├── tours.py            # Tour packages blueprint
│   ├── bookings.py         # Bookings & payments blueprint
│   ├── admin.py            # Admin dashboard & inquiries blueprint
│   ├── reviews.py          # Reviews blueprint
│   ├── email_service.py    # (Optional) Email logic
│   └── templates/
│       ├── base.html
│       ├── auth/
│       ├── tours/
│       ├── bookings/
│       ├── admin/
│       └── reviews/
│
├── static/                 # CSS, JS, images
├── requirements.txt
├── config.py
├── run.py                  # Entry point
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
