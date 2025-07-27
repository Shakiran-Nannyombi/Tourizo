from datetime import datetime, timedelta
import secrets
import string
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db
from app.extensions import login_manager
import logging

logger = logging.getLogger(__name__)

wishlist_table = db.Table('wishlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('tour_id', db.Integer, db.ForeignKey('tour.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    account_locked = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(20))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    bio = db.Column(db.Text)
    
    # Settings fields
    email_notifications = db.Column(db.Boolean, default=True)
    newsletter = db.Column(db.Boolean, default=False)
    sms_notifications = db.Column(db.Boolean, default=False)
    language = db.Column(db.String(10), default='en')
    timezone = db.Column(db.String(20), default='UTC')
    two_factor_auth = db.Column(db.Boolean, default=False)
    public_profile = db.Column(db.Boolean, default=True)
    
    # Timestamps
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    inquiries = db.relationship('Inquiry', backref='user', lazy=True)
    wishlist = db.relationship('Tour', secondary=wishlist_table, lazy='subquery',
                              backref=db.backref('wishlisted_by', lazy=True))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.login_attempts = 0
        self.account_locked = False

    def set_password(self, password):
        """Create a secure password hash using scrypt"""
        try:
            self.password_hash = generate_password_hash(
                password,
                method='scrypt',
                salt_length=16
            )
            logger.info(f"Password hash updated for user {self.email}")
        except Exception as e:
            logger.error(f"Failed to set password: {str(e)}")
            raise

    def check_password(self, password):
        """Verify password and upgrade hash if needed"""
        if not password or not self.password_hash:
            logger.warning("Missing password or hash")
            return False

        try:
            valid = check_password_hash(self.password_hash, password)

            if valid:
                logger.info(f"✅ Password verified for {self.email}")
                self.last_login = datetime.utcnow()
                self.login_attempts = 0

                if not self.password_hash.startswith('scrypt:'):
                    logger.info(f"⬆️ Upgrading hash for {self.email} to scrypt")
                    self.set_password(password)

                db.session.commit()
                return True
            else:
                logger.warning(f"❌ Invalid password attempt for {self.email}")
                self.login_attempts = (self.login_attempts or 0) + 1
                if self.login_attempts >= 5:
                    self.account_locked = True
                    logger.warning(f"🔒 Account locked for {self.email}")
                db.session.commit()
                return False

        except Exception as e:
            logger.error(f"🚨 Password check failed: {str(e)}")
            db.session.rollback()
            return False

    def needs_password_upgrade(self):
        """Check if password hash needs to be upgraded to newer format"""
        return not self.password_hash.startswith('scrypt:')

    def reset_login_attempts(self):
        """Reset failed login attempts counter"""
        self.login_attempts = 0
        self.account_locked = False
        db.session.commit()
        logger.info(f"Reset login attempts for {self.email}")

    def generate_password_reset_token(self):
        """Generate a secure password reset token"""
        self.otp_code = ''.join(secrets.choice(string.digits) for _ in range(8))
        self.otp_expiry = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()
        return self.otp_code

    def verify_otp(self, otp):
        """Verify OTP code with expiry check"""
        if not self.otp_code or not self.otp_expiry:
            return False

        if datetime.utcnow() > self.otp_expiry:
            return False

        return secrets.compare_digest(self.otp_code, otp)

    @property
    def is_active(self):
        return bool(self.__dict__.get('is_active', True))

    @classmethod
    def create_test_user(cls, username, email, password, is_admin=False):
        """Create a test user with admin flag"""
        try:
            user = cls(
                username=username,
                email=email,
                is_admin=is_admin
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            logger.info(f"Created test user: {email}")
            return user
        except Exception as e:
            logger.error(f"Failed to create test user: {str(e)}")
            db.session.rollback()
            return None

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        logger.error(f"Failed to load user {user_id}: {str(e)}")
        return None
