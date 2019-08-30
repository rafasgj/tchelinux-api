"""Migrate database to system version 0.1.

Revision ID: 61c21012b79d
Revises:
Create Date: 2019-05-12 21:17:24.880682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61c21012b79d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    Create first version of the database.

    The following changes are made to the database:
        - Create table 'events'.
        - Create table 'cities'.
        - Create table 'institutions'.
    """
    op.create_table(
        'cities',
        sa.Column('cname', sa.String, primary_key=True),
        sa.Column('name', sa.String),

    )
    op.create_table(
        'institutions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String),
        sa.Column('nick', sa.String, nullable=False),
        sa.Column('address', sa.String, nullable=False),
        sa.Column('city', sa.String),
    )
    op.create_table(
        'events',
        sa.Column('date', sa.Date, primary_key=True),
        sa.Column('institution_id', sa.Integer)
    )
    # Create foreign keys.
    op.create_foreign_key("fk_intituicao_city", "institutions", "cities",
                          ["city"], ['cname'], ondelete="CASCADE")
    op.create_foreign_key("fk_event_institutions", "events", "institutions",
                          ["institution_id"], ['id'], ondelete="CASCADE")


def downgrade():
    """Downgrade database to previous version."""
    op.drop_table('events')
    op.drop_table('institutions')
    op.drop_table('cities')
