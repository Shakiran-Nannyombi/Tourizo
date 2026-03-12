"""Create all required database tables

Revision ID: create_all_tables
Revises: d181f4666337
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'create_all_tables'
down_revision = None  # This is now the FIRST migration
branch_labels = None
depends_on = None


def upgrade():
    # Get database connection and inspector to check existing tables
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()
    
    print(f"DEBUG: Existing tables before migration: {existing_tables}")
    
    # 1. Create Category table (no dependencies)
    if 'category' not in existing_tables:
        print("DEBUG: Creating category table...")
        op.create_table(
            'category',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('name')
        )
        print("DEBUG: Category table created!")
    else:
        print("DEBUG: Category table already exists, skipping...")
    
    # 2. Create User table (no dependencies)
    if 'user' not in existing_tables:
        op.create_table(
            'user',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('username', sa.String(length=80), nullable=False),
            sa.Column('email', sa.String(length=120), nullable=False),
            sa.Column('password_hash', sa.String(length=255), nullable=False),
            sa.Column('is_admin', sa.Boolean(), nullable=True, server_default=sa.false()),
            sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.true()),
            sa.Column('account_locked', sa.Boolean(), nullable=True, server_default=sa.false()),
            sa.Column('phone', sa.String(length=20), nullable=True),
            sa.Column('first_name', sa.String(length=50), nullable=True),
            sa.Column('last_name', sa.String(length=50), nullable=True),
            sa.Column('date_of_birth', sa.Date(), nullable=True),
            sa.Column('bio', sa.Text(), nullable=True),
            sa.Column('email_notifications', sa.Boolean(), nullable=True, server_default=sa.true()),
            sa.Column('newsletter', sa.Boolean(), nullable=True, server_default=sa.false()),
            sa.Column('sms_notifications', sa.Boolean(), nullable=True, server_default=sa.false()),
            sa.Column('language', sa.String(length=10), nullable=True, server_default='en'),
            sa.Column('timezone', sa.String(length=20), nullable=True, server_default='UTC'),
            sa.Column('two_factor_auth', sa.Boolean(), nullable=True, server_default=sa.false()),
            sa.Column('public_profile', sa.Boolean(), nullable=True, server_default=sa.true()),
            sa.Column('date_created', sa.DateTime(), nullable=True),
            sa.Column('last_login', sa.DateTime(), nullable=True),
            sa.Column('otp_code', sa.String(length=8), nullable=True),
            sa.Column('otp_expiry', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email'),
            sa.UniqueConstraint('username')
        )
    
    # 3. Create Destination table (no dependencies)
    if 'destination' not in existing_tables:
        op.create_table(
            'destination',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=200), nullable=False),
            sa.Column('country', sa.String(length=100), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('name')
        )
    
    # 4. Create ChatbotSettings table (no dependencies)
    if 'chatbot_settings' not in existing_tables:
        op.create_table(
            'chatbot_settings',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('groq_api_key', sa.String(length=128), nullable=False),
            sa.Column('groq_model', sa.String(length=64), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )
    
    # 5. Create TourPackage table (no dependencies)
    if 'tour_package' not in existing_tables:
        op.create_table(
            'tour_package',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=120), nullable=False),
            sa.Column('description', sa.Text(), nullable=False),
            sa.Column('price', sa.Float(), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )
    
    # 6. Create Tour table (depends on Category)
    if 'tour' not in existing_tables:
        op.create_table(
            'tour',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=200), nullable=False),
            sa.Column('description', sa.Text(), nullable=False),
            sa.Column('short_description', sa.String(length=300), nullable=True),
            sa.Column('price', sa.Float(), nullable=False),
            sa.Column('duration', sa.Integer(), nullable=False),
            sa.Column('duration_type', sa.String(length=20), nullable=True, server_default='Days'),
            sa.Column('max_participants', sa.Integer(), nullable=True, server_default='20'),
            sa.Column('min_participants', sa.Integer(), nullable=True, server_default='1'),
            sa.Column('difficulty_level', sa.String(length=20), nullable=True, server_default='Easy'),
            sa.Column('departure_location', sa.String(length=200), nullable=True),
            sa.Column('image', sa.String(length=200), nullable=True),
            sa.Column('image_gallery', sa.Text(), nullable=True),
            sa.Column('inclusions', sa.Text(), nullable=True),
            sa.Column('exclusions', sa.Text(), nullable=True),
            sa.Column('itinerary', sa.Text(), nullable=True),
            sa.Column('available_from', sa.Date(), nullable=True),
            sa.Column('available_to', sa.Date(), nullable=True),
            sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.true()),
            sa.Column('is_featured', sa.Boolean(), nullable=True, server_default=sa.false()),
            sa.Column('meta_title', sa.String(length=200), nullable=True),
            sa.Column('meta_description', sa.String(length=300), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.Column('category_id', sa.Integer(), nullable=False),
            sa.Column('destination', sa.String(length=100), nullable=False),
            sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
    
    # 7. Create TourDate table (depends on Tour)
    if 'tour_date' not in existing_tables:
        op.create_table(
            'tour_date',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('tour_id', sa.Integer(), nullable=False),
            sa.Column('date', sa.Date(), nullable=False),
            sa.Column('available_spots', sa.Integer(), nullable=False),
            sa.Column('price_override', sa.Float(), nullable=True),
            sa.Column('is_available', sa.Boolean(), nullable=True, server_default=sa.true()),
            sa.ForeignKeyConstraint(['tour_id'], ['tour.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
    
    # 8. Create TourItineraryDay table (depends on Tour)
    if 'tour_itinerary_day' not in existing_tables:
        op.create_table(
            'tour_itinerary_day',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('tour_id', sa.Integer(), nullable=False),
            sa.Column('day', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=200), nullable=False),
            sa.Column('description', sa.Text(), nullable=False),
            sa.ForeignKeyConstraint(['tour_id'], ['tour.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
    
    # 9. Create Booking table (depends on Tour, User)
    if 'booking' not in existing_tables:
        op.create_table(
            'booking',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('reference', sa.String(length=36), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=True),
            sa.Column('tour_id', sa.Integer(), nullable=False),
            sa.Column('full_name', sa.String(length=200), nullable=False),
            sa.Column('email', sa.String(length=120), nullable=False),
            sa.Column('phone', sa.String(length=30), nullable=False),
            sa.Column('booking_date', sa.Date(), nullable=False),
            sa.Column('booking_time', sa.Time(), nullable=True),
            sa.Column('num_people', sa.Integer(), nullable=False, server_default='1'),
            sa.Column('special_requests', sa.Text(), nullable=True),
            sa.Column('total_amount', sa.Numeric(precision=10, scale=2), nullable=False),
            sa.Column('payment_method', sa.String(length=20), nullable=True),
            sa.Column('payment_status', sa.String(length=20), nullable=False, server_default='pending'),
            sa.Column('payment_reference', sa.String(length=100), nullable=True),
            sa.Column('payment_details', sa.String(length=255), nullable=True),
            sa.Column('order_tracking_id', sa.String(length=100), nullable=True),
            sa.Column('cancellation_reason', sa.String(length=50), nullable=True),
            sa.Column('cancellation_notes', sa.Text(), nullable=True),
            sa.Column('cancelled_at', sa.DateTime(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['tour_id'], ['tour.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('reference')
        )
    
    # 10. Create Review table (depends on Tour, User)
    if 'review' not in existing_tables:
        op.create_table(
            'review',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('rating', sa.Integer(), nullable=False),
            sa.Column('comment', sa.Text(), nullable=True),
            sa.Column('reviewer_name', sa.String(length=100), nullable=False),
            sa.Column('reviewer_email', sa.String(length=120), nullable=True),
            sa.Column('is_verified', sa.Boolean(), nullable=True, server_default=sa.false()),
            sa.Column('is_approved', sa.Boolean(), nullable=True, server_default=sa.false()),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('tour_id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['tour_id'], ['tour.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
    
    # 11. Create Wishlist table (depends on User, Tour)
    if 'wishlist' not in existing_tables:
        op.create_table(
            'wishlist',
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('tour_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['tour_id'], ['tour.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('user_id', 'tour_id')
        )
    
    # 12. Create Inquiry table (depends on User)
    if 'inquiries' not in existing_tables:
        op.create_table(
            'inquiries',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('email', sa.String(length=120), nullable=False),
            sa.Column('message', sa.Text(), nullable=False),
            sa.Column('timestamp', sa.DateTime(), nullable=True),
            sa.Column('user_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade():
    # Drop tables in reverse dependency order
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()
    
    if 'inquiries' in existing_tables:
        op.drop_table('inquiries')
    if 'wishlist' in existing_tables:
        op.drop_table('wishlist')
    if 'review' in existing_tables:
        op.drop_table('review')
    if 'booking' in existing_tables:
        op.drop_table('booking')
    if 'tour_itinerary_day' in existing_tables:
        op.drop_table('tour_itinerary_day')
    if 'tour_date' in existing_tables:
        op.drop_table('tour_date')
    if 'tour' in existing_tables:
        op.drop_table('tour')
    if 'tour_package' in existing_tables:
        op.drop_table('tour_package')
    if 'chatbot_settings' in existing_tables:
        op.drop_table('chatbot_settings')
    if 'destination' in existing_tables:
        op.drop_table('destination')
    if 'user' in existing_tables:
        op.drop_table('user')
    if 'category' in existing_tables:
        op.drop_table('category')
