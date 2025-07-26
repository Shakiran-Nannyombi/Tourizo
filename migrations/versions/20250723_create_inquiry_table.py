"""create inquiries table

Revision ID: add_inquiry_table
Revises: 995e75c4bda2  # or your latest revision ID
Create Date: 2025-07-23

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_inquiry_table'
down_revision = '995e75c4bda2'  # replace with your last migration id
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'inquiries',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('inquiries')
