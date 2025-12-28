#!/usr/bin/env python
"""Check database status"""
from app import create_app, db
from app.models.Tour import Tour
from app.models.Category import Category
from app.models.Booking import Booking
from app.models.User import User
from app.models.Review import Review

app = create_app()

with app.app_context():
    print('=' * 80)
    print('DATABASE SUMMARY')
    print('=' * 80)
    print(f'Users:      {User.query.count()}')
    print(f'Categories: {Category.query.count()}')
    print(f'Tours:      {Tour.query.count()}')
    print(f'Bookings:   {Booking.query.count()}')
    print(f'Reviews:    {Review.query.count()}')
    
    print('\n' + '=' * 80)
    print('CATEGORIES')
    print('=' * 80)
    for c in Category.query.all():
        print(f'  ✓ {c.name}')
    
    print('\n' + '=' * 80)
    print('TOURS')
    print('=' * 80)
    for t in Tour.query.all():
        print(f'  ✓ {t.title} (${t.price})')
    
    print('\n' + '=' * 80)
    print('BOOKINGS BY STATUS')
    print('=' * 80)
    paid = Booking.query.filter_by(payment_status='Paid').count()
    pending = Booking.query.filter_by(payment_status='Pending').count()
    cancelled = Booking.query.filter_by(payment_status='Cancelled').count()
    print(f'  Paid:      {paid}')
    print(f'  Pending:   {pending}')
    print(f'  Cancelled: {cancelled}')
    print('=' * 80)
