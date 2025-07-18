"""Merge migration branches

Revision ID: 144b19ab5fde
Revises: 33e4476f651f, f92f5d48952a
Create Date: 2025-07-18 09:15:11.184279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '144b19ab5fde'
down_revision = ('33e4476f651f', 'f92f5d48952a')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
