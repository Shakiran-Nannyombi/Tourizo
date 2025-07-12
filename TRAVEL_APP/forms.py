from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (StringField, TextAreaField, FloatField, IntegerField, 
                     SelectField, DateField, BooleanField, SubmitField, 
                     MultipleFileField, FieldList, FormField)
from wtforms.validators import DataRequired, Length, NumberRange, Email, Optional, ValidationError
from wtforms.widgets import TextArea
from datetime import date

class TourForm(FlaskForm):
    """Form for adding/editing tour packages"""
    
    title = StringField('Tour Title', validators=[
        DataRequired(message='Title is required'),
        Length(min=5, max=200, message='Title must be between 5 and 200 characters')
    ])
    
    short_description = TextAreaField('Short Description', validators=[
        Length(max=300, message='Short description must be less than 300 characters')
    ])
    
    description = TextAreaField('Full Description', validators=[
        DataRequired(message='Description is required')
    ])
    
    # FIXED: Change to SelectField to match destination_id in model
    # ✅ Updated: Allow free text entry for destination
    destination = StringField('Destination', validators=[
    DataRequired(message='Destination is required'),
    Length(max=100, message='Destination must be less than 100 characters')
])

    # FIXED: Change to SelectField for consistency
    departure_location = StringField('Departure Location', validators=[
    DataRequired(message='Departure location is required'),
    Length(max=100, message='Departure location must be less than 100 characters')
])

    category_id = SelectField('Category', coerce=int, validators=[
        DataRequired(message='Category is required')
    ])
    
    price = FloatField('Price (USD)', validators=[
        DataRequired(message='Price is required'),
        NumberRange(min=0, message='Price must be positive')
    ])
    
    duration = IntegerField('Duration', validators=[
        DataRequired(message='Duration is required'),
        NumberRange(min=1, message='Duration must be at least 1')
    ])
    
    # FIXED: Add choices that will be set in the route
    duration_type = SelectField('Duration Type', validators=[
        DataRequired(message='Duration type is required')
    ])
    
    max_participants = IntegerField('Maximum Participants', validators=[
        DataRequired(message='Maximum participants is required'),
        NumberRange(min=1, message='Must accommodate at least 1 person')
    ])
    
    min_participants = IntegerField('Minimum Participants', validators=[
        DataRequired(message='Minimum participants is required'),
        NumberRange(min=1, message='Must require at least 1 person')
    ])
    
    # FIXED: Add choices that will be set in the route
    difficulty_level = SelectField('Difficulty Level', validators=[
        DataRequired(message='Difficulty level is required')
    ])
    
    featured_image = FileField('Featured Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 
                   'Only image files are allowed')
    ])
    
    gallery_images = MultipleFileField('Gallery Images', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 
                   'Only image files are allowed')
    ])
    
    inclusions = TextAreaField('What\'s Included', 
                              description='Enter each inclusion on a new line')
    
    exclusions = TextAreaField('What\'s Not Included', 
                              description='Enter each exclusion on a new line')
    
    itinerary = TextAreaField('Itinerary', 
                             description='Describe the day-by-day itinerary')
    
    available_from = DateField('Available From', validators=[Optional()])
    available_to = DateField('Available To', validators=[Optional()])
    
    is_active = BooleanField('Active', default=True)
    is_featured = BooleanField('Featured Package', default=False)
    
    meta_title = StringField('Meta Title (SEO)', validators=[
        Length(max=200, message='Meta title must be less than 200 characters')
    ])
    
    meta_description = TextAreaField('Meta Description (SEO)', validators=[
        Length(max=300, message='Meta description must be less than 300 characters')
    ])
    
    submit = SubmitField('Save Tour Package')
    
    def validate_available_to(self, field):
        if field.data and self.available_from.data:
            if field.data <= self.available_from.data:
                raise ValidationError('End date must be after start date')
    
    def validate_min_participants(self, field):
        if field.data and self.max_participants.data:
            if field.data > self.max_participants.data:
                raise ValidationError('Minimum participants cannot exceed maximum')

class CategoryForm(FlaskForm):
    """Form for adding/editing categories"""
    
    name = StringField('Category Name', validators=[
        DataRequired(message='Category name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    description = TextAreaField('Description', validators=[
        Length(max=500, message='Description must be less than 500 characters')
    ])
    
    submit = SubmitField('Save Category')

class TourSearchForm(FlaskForm):
    """Form for searching and filtering tours"""
    
    search = StringField('Search Tours', validators=[
        Length(max=200, message='Search term too long')
    ])
    
    category = SelectField('Category', coerce=int, validators=[Optional()])
    
    min_price = FloatField('Min Price', validators=[
        Optional(),
        NumberRange(min=0, message='Price must be positive')
    ])
    
    max_price = FloatField('Max Price', validators=[
        Optional(),
        NumberRange(min=0, message='Price must be positive')
    ])
    
    duration_min = IntegerField('Min Duration', validators=[
        Optional(),
        NumberRange(min=1, message='Duration must be at least 1')
    ])
    
    duration_max = IntegerField('Max Duration', validators=[
        Optional(),
        NumberRange(min=1, message='Duration must be at least 1')
    ])
    
    difficulty = SelectField('Difficulty', choices=[
        ('', 'Any Difficulty'),
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
        ('Expert', 'Expert')
    ], default='')
    
    sort_by = SelectField('Sort By', choices=[
        ('created_at', 'Newest First'),
        ('price_asc', 'Price: Low to High'),
        ('price_desc', 'Price: High to Low'),
        ('duration_asc', 'Duration: Short to Long'),
        ('duration_desc', 'Duration: Long to Short'),
        ('title', 'Title A-Z')
    ], default='created_at')
    
    submit = SubmitField('Search')

class BookingForm(FlaskForm):
    """Form for booking tours"""
    
    customer_name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=200, message='Name must be between 2 and 200 characters')
    ])
    
    customer_email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    customer_phone = StringField('Phone Number', validators=[
        Length(max=20, message='Phone number too long')
    ])
    
    tour_date = DateField('Preferred Tour Date', validators=[
        DataRequired(message='Tour date is required')
    ])
    
    participants = IntegerField('Number of Participants', validators=[
        DataRequired(message='Number of participants is required'),
        NumberRange(min=1, message='Must have at least 1 participant')
    ])
    
    special_requests = TextAreaField('Special Requests', validators=[
        Length(max=1000, message='Special requests too long')
    ])
    
    submit = SubmitField('Book Now')
    
    def validate_tour_date(self, field):
        if field.data and field.data < date.today():
            raise ValidationError('Tour date cannot be in the past')

class ReviewForm(FlaskForm):
    """Form for submitting reviews"""
    
    rating = SelectField('Rating', choices=[
        (5, '5 Stars - Excellent'),
        (4, '4 Stars - Good'),
        (3, '3 Stars - Average'),
        (2, '2 Stars - Poor'),
        (1, '1 Star - Terrible')
    ], coerce=int, validators=[DataRequired()])
    
    reviewer_name = StringField('Your Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    reviewer_email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    comment = TextAreaField('Your Review', validators=[
        Length(max=1000, message='Review must be less than 1000 characters')
    ])
    
    submit = SubmitField('Submit Review')

class TourDateForm(FlaskForm):
    """Form for managing specific tour dates"""
    
    date = DateField('Date', validators=[DataRequired()])
    available_spots = IntegerField('Available Spots', validators=[
        DataRequired(),
        NumberRange(min=0, message='Spots must be non-negative')
    ])
    price_override = FloatField('Price Override (Optional)', validators=[
        Optional(),
        NumberRange(min=0, message='Price must be positive')
    ])
    is_available = BooleanField('Available', default=True)
    
    submit = SubmitField('Save Date')
    
    def validate_date(self, field):
        if field.data and field.data < date.today():
            raise ValidationError('Date cannot be in the past')