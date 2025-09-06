"""add last login field

Revision ID: add_last_login_field
Revises: initial_migration
Create Date: 2025-09-06 22:13:49.461000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = 'add_last_login_field'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add last_login column with current timestamp as default
    op.add_column('users', sa.Column('last_login', sa.DateTime(timezone=True), server_default=func.now()))


def downgrade() -> None:
    # Remove last_login column
    op.drop_column('users', 'last_login')
