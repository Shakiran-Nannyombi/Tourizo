"""add chatbotsettings table

Revision ID: chatbotsettings_20250727
Revises: 
Create Date: 2025-07-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'chatbotsettings_20250727'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'chatbot_settings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('groq_api_key', sa.String(length=128), nullable=False),
        sa.Column('groq_model', sa.String(length=64), nullable=False)
    )

def downgrade():
    op.drop_table('chatbot_settings') 