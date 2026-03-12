"""add chatbotsettings table

Revision ID: chatbotsettings_20250727
Revises: create_all_tables
Create Date: 2025-07-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'chatbotsettings_20250727'
down_revision = 'create_all_tables'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()
    
    if 'chatbot_settings' not in existing_tables:
        op.create_table(
            'chatbot_settings',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('groq_api_key', sa.String(length=128), nullable=False),
            sa.Column('groq_model', sa.String(length=64), nullable=False)
        )

def downgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()
    
    if 'chatbot_settings' in existing_tables:
        op.drop_table('chatbot_settings') 