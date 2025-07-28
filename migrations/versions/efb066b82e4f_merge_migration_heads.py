"""Merge migration heads

Revision ID: efb066b82e4f
Revises: chatbotsettings_20250727, 33fb3c63df00, c6f36bdf7acb
Create Date: 2025-07-28 17:10:13.642382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efb066b82e4f'
down_revision = ('chatbotsettings_20250727', '33fb3c63df00', 'c6f36bdf7acb')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
