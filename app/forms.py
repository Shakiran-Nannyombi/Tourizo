from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, FloatField, IntegerField, PasswordField,
    SelectField, DateField, BooleanField, SubmitField,
    MultipleFileField, HiddenField
)
from wtforms.validators import (
    DataRequired, Length, NumberRange, Email, Optional,
    ValidationError, Regexp,EqualTo
)
from wtforms.fields import TimeField
from wtforms.widgets import TextArea, Input
from datetime import date


# ✅ Fixed: Custom telephone input with validation_attrs
class TelInput(Input):
    input_type = 'tel'
    validation_attrs = frozenset(['required', 'maxlength', 'minlength', 'pattern'])


class TelField(StringField):
    widget = TelInput()


# Custom Validators
def _pin_validator(form, field):
    provider = form.provider.data
    pin = field.data or ""
    if provider == "airtel" and len(pin) != 4:
        raise ValidationError("Airtel PIN must be 4 digits.")
    if provider == "mtn" and len(pin) != 5:
        raise ValidationError("MTN PIN must be 5 digits.")


def _date_validator(form, field):
    if field.data and field.data < date.today():
        raise ValidationError("Booking date cannot be in the past.")


# Tour Form
class TourForm(FlaskForm):
    title = StringField('Tour Title', validators=[DataRequired(), Length(min=5, max=200)])
    short_description = TextAreaField('Short Description', validators=[Length(max=300)])
    description = TextAreaField('Full Description', validators=[DataRequired()])
    destination = StringField('Destination', validators=[DataRequired(), Length(max=100)])
    departure_location = StringField('Departure Location', validators=[DataRequired(), Length(max=100)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    price = FloatField('Price (USD)', validators=[DataRequired(), NumberRange(min=0)])
    duration = IntegerField('Duration', validators=[DataRequired(), NumberRange(min=1)])
    duration_type = SelectField('Duration Type', validators=[DataRequired()])
    max_participants = IntegerField('Maximum Participants', validators=[DataRequired(), NumberRange(min=1)])
    min_participants = IntegerField('Minimum Participants', validators=[DataRequired(), NumberRange(min=1)])
    difficulty_level = SelectField('Difficulty Level', validators=[DataRequired()])
    featured_image = FileField('Featured Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Only image files are allowed')
    ])
    gallery_images = MultipleFileField('Gallery Images', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Only image files are allowed')
    ])
    inclusions = TextAreaField("What's Included")
    exclusions = TextAreaField("What's Not Included")
    itinerary = TextAreaField("Itinerary")
    available_from = DateField('Available From', validators=[Optional()])
    available_to = DateField('Available To', validators=[Optional()])
    is_active = BooleanField('Active', default=True)
    is_featured = BooleanField('Featured Package', default=False)
    meta_title = StringField('Meta Title (SEO)', validators=[Length(max=200)])
    meta_description = TextAreaField('Meta Description (SEO)', validators=[Length(max=300)])
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
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    submit = SubmitField('Save Category')


class TourSearchForm(FlaskForm):
    search = StringField('Search Tours', validators=[Length(max=200)])
    category = SelectField('Category', coerce=int, validators=[Optional()])
    min_price = FloatField('Min Price', validators=[Optional(), NumberRange(min=0)])
    max_price = FloatField('Max Price', validators=[Optional(), NumberRange(min=0)])
    duration_min = IntegerField('Min Duration', validators=[Optional(), NumberRange(min=1)])
    duration_max = IntegerField('Max Duration', validators=[Optional(), NumberRange(min=1)])
    difficulty = SelectField('Difficulty', choices=[
        ('', 'Any Difficulty'), ('Easy', 'Easy'), ('Medium', 'Medium'),
        ('Hard', 'Hard'), ('Expert', 'Expert')
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
    def __init__(self, require_payment_method=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not require_payment_method:
            self.payment_method.validators = [Optional()]

    full_name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = TelField("Phone", validators=[DataRequired(), Regexp(r"^\+?\d{7,15}$")])
    num_people = IntegerField("Number of People", validators=[DataRequired(), NumberRange(min=1)])
    booking_date = DateField("Tour Date", validators=[DataRequired(), _date_validator])
    booking_time = TimeField("Start Time", validators=[DataRequired()])
    tour_id = SelectField('Tour', coerce=int, validators=[DataRequired()])
    card_token = HiddenField()
    momo_token = HiddenField()
    payment_method = SelectField("Payment Method", choices=[
        ("momo", "Mobile Money"),
        ("card", "Credit Card")
    ], validators=[DataRequired()])
    special_requests = TextAreaField('Special Requests', validators=[Optional()])
    submit = SubmitField("Book Now")


class CreditCardForm(FlaskForm):
    card_number = StringField("Card Number", validators=[
        DataRequired(), Regexp(r"^\d{13,19}$", message="Enter 13–19 digits")
    ])
    expiry = StringField("Expiry Date", validators=[
        DataRequired(), Regexp(r"^(0[1-9]|1[0-2])\/\d{2}$", message="Use MM/YY format")
    ])
    cvc = PasswordField("Security Code", validators=[
        DataRequired(), Regexp(r"^\d{3,4}$", message="Enter 3–4 digits")
    ])
    save_card = SubmitField("Save Card")


class PaymentForm(FlaskForm):
    booking_id = HiddenField(validators=[DataRequired()])
    payment_method = SelectField("Payment Method", choices=[
        ("", "Select..."), ("momo", "Mobile Money"), ("card", "Credit Card")
    ], validators=[DataRequired()])
    momo_number = TelField("MoMo Number", validators=[Optional()])
    card_number = StringField("Card Number", validators=[Optional()])
    submit = SubmitField("Pay")


class MobileMoneyForm(FlaskForm):
    provider = SelectField("Mobile Provider", choices=[
        ("", "Select provider..."), ("mtn", "MTN MoMo"), ("airtel", "Airtel Money")
    ], validators=[DataRequired()])
    momo_number = TelField("Mobile Number", validators=[
        DataRequired(), Regexp(r"^\+?\d{9,15}$", message="Enter a valid mobile number")
    ])
    pin = PasswordField("PIN", validators=[
        DataRequired(), Regexp(r"^\d{4,5}$"), _pin_validator
    ])
    save_momo = SubmitField("Save MoMo")


class CancelForm(FlaskForm):
    reason = SelectField('Cancellation Reason', choices=[
        ('', 'Select reason...'), ('plans_changed', 'My plans changed'),
        ('found_better', 'Found a better option'), ('unhappy_service', 'Unhappy with service'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    notes = TextAreaField('Additional Notes')
    confirm = BooleanField('I confirm I want to cancel', validators=[
        DataRequired(message="You must confirm the cancellation")
    ])
    submit = SubmitField('Submit Cancellation')


class DeleteForm(FlaskForm):
    """CSRF protection only"""
    pass


class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        (5, '5 Stars - Excellent'), (4, '4 Stars - Good'),
        (3, '3 Stars - Average'), (2, '2 Stars - Poor'), (1, '1 Star - Terrible')
    ], coerce=int, validators=[DataRequired()])
    reviewer_name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=100)])
    reviewer_email = StringField('Email Address', validators=[DataRequired(), Email()])
    comment = TextAreaField('Your Review', validators=[Length(max=1000)])
    submit = SubmitField('Submit Review')


class TourDateForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    available_spots = IntegerField('Available Spots', validators=[DataRequired(), NumberRange(min=0)])
    price_override = FloatField('Price Override (Optional)', validators=[Optional(), NumberRange(min=0)])
    is_available = BooleanField('Available', default=True)
    submit = SubmitField('Save Date')

    def validate_date(self, field):
        if field.data and field.data < date.today():
            raise ValidationError('Date cannot be in the past')
# At the bottom of your forms file
class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(min=7, max=15)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])

    password = PasswordField('New Password', validators=[
        Optional(),
        Length(min=6, message='Password should be at least 6 characters'),
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        Optional(),
        EqualTo('password', message='Passwords must match')
    ])

    submit = SubmitField('Update Profile')
    
class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
