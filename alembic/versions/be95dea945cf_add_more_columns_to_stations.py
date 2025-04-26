"""Add More Columns to Stations

Revision ID: be95dea945cf
Revises: 
Create Date: 2025-04-21 17:17:18.808632

"""
from email.policy import default
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer

# revision identifiers, used by Alembic.
revision: str = 'be95dea945cf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('stations', sa.Column('x'), Integer(), default=20, postgresql_after='existing_column_name')
    op.add_column('stations', sa.Column('y'), Integer(), default=20)
    op.add_column('stations', sa.Column('width'), Integer(), default=300)
    op.add_column('stations', sa.Column('x'), Integer(), default=200)
    op.add_column('stations', sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()))
    op.add_column('stations', sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()))

def downgrade() -> None:
    """Downgrade schema."""
    pass
