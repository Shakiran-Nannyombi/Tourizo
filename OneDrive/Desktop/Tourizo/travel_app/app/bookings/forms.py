from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, SelectField, TelField, SubmitField,
    PasswordField, HiddenField, TextAreaField, BooleanField
)
from wtforms.validators import (
    DataRequired, Email, NumberRange, Regexp, ValidationError
)
from wtforms.fields import DateField, TimeField
from datetime import date, time
from wtforms.validators import Optional


# Helper – provider-specific PIN length
def _pin_validator(form, field):
    provider = form.provider.data
    pin = field.data or ""

    if provider == "airtel" and len(pin) != 4:
        raise ValidationError("Airtel PIN must be 4 digits.")
    if provider == "mtn" and len(pin) != 5:
        raise ValidationError("MTN PIN must be 5 digits.")

# Date validator to ensure booking is not in the past
def _date_validator(form, field):
    if field.data and field.data < date.today():
        raise ValidationError("Booking date cannot be in the past.")

class BookingForm(FlaskForm):
    def __init__(self, require_payment_method=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not require_payment_method:
            self.payment_method.validators = [Optional()]

    full_name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = TelField("Phone", validators=[DataRequired(), Regexp(r"^\+?\d{7,15}$")])
    num_people = IntegerField("Number of People", validators=[DataRequired(), NumberRange(min=1)])
    package_id = SelectField("Tour Package", coerce=int, validators=[DataRequired()])
    booking_date = DateField("Tour Date", validators=[DataRequired(), _date_validator])
    booking_time = TimeField("Start Time", validators=[DataRequired()])
    payment_method = SelectField(
        "Payment Method",
        choices=[("", "Select payment method..."), ("card", "Credit Card"), ("momo", "Mobile Money")],
        validators=[DataRequired()]
    )
    card_token = HiddenField()
    momo_token = HiddenField()
    submit = SubmitField("Book Now")

class CreditCardForm(FlaskForm):
    card_number = StringField(
        "Card Number",
        validators=[
            DataRequired(),
            Regexp(r"^\d{13,19}$", message="Enter 13–19 digits"),
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'style': 'border-color: #a5c4a0;'
        }
    )
    
    expiry = StringField(
        "Expiry Date",
        validators=[
            DataRequired(),
            Regexp(r"^(0[1-9]|1[0-2])\/\d{2}$", message="Use MM/YY format"),
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'MM/YY',
            'style': 'border-color: #a5c4a0;'
        }
    )
    
    cvc = PasswordField(
        "Security Code",
        validators=[
            DataRequired(),
            Regexp(r"^\d{3,4}$", message="Enter 3–4 digits"),
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'CVC',
            'style': 'border-color: #a5c4a0;'
        }
    )
    
    save_card = SubmitField(
        "Save Card",
        render_kw={
            'class': 'btn',
            'style': 'background-color: #588157; color: white;'
        }
    )

class MobileMoneyForm(FlaskForm):
    provider = SelectField(
        "Mobile Provider",
        choices=[
            ("", "Select provider..."),
            ("mtn", "MTN MoMo"),
            ("airtel", "Airtel Money"),
        ],
        validators=[DataRequired()],
        render_kw={
            'class': 'form-select',
            'style': 'border-color: #a5c4a0;'
        }
    )
    
    momo_number = TelField(
        "Mobile Number",
        validators=[
            DataRequired(),
            Regexp(r"^\+?\d{9,15}$", message="Enter a valid mobile number"),
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '+256 XXX XXX XXX',
            'style': 'border-color: #a5c4a0;'
        }
    )
    
    pin = PasswordField(
        "PIN",
        validators=[
            DataRequired(),
            Regexp(r"^\d{4,5}$"),
            _pin_validator,
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter PIN',
            'style': 'border-color: #a5c4a0;'
        }
    )
    
    save_momo = SubmitField(
        "Save MoMo",
        render_kw={
            'class': 'btn',
            'style': 'background-color: #588157; color: white;'
        }
    )

class CancelForm(FlaskForm):
    reason = SelectField(
        'Cancellation Reason',
        choices=[
            ('', 'Select reason...'),
            ('plans_changed', 'My plans changed'),
            ('found_better', 'Found a better option'),
            ('unhappy_service', 'Unhappy with service'),
            ('other', 'Other')
        ],
        validators=[DataRequired(message="Please select a cancellation reason")],
        render_kw={
            'class': 'form-select',
            'style': 'border-color: #a5c4a0;'
        }
    )
    
    notes = TextAreaField(
        'Additional Notes',
        render_kw={
            'class': 'form-control',
            'rows': 3,
            'style': 'border-color: #a5c4a0;'
        }
    )
    
    confirm = BooleanField(
        'I confirm I want to cancel',
        validators=[DataRequired(message="You must confirm the cancellation")],
        render_kw={
            'class': 'form-check-input',
            'style': 'border-color: #a5c4a0;'
        }
    )
    
    submit = SubmitField(
        'Submit Cancellation',
        render_kw={
            'class': 'btn',
            'style': 'background-color: #d4a59a; color: white;'
        }
    )

class DeleteForm(FlaskForm):
    """Simple form just for CSRF protection during deletions"""
    pass