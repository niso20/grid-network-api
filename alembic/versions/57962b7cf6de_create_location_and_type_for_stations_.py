"""Create Location and type for stations table

Revision ID: 57962b7cf6de
Revises: be95dea945cf
Create Date: 2025-05-13 15:41:04.941128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String
from enums.StationType import StationType

# revision identifiers, used by Alembic.
revision: str = '57962b7cf6de'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('stations', sa.Column('location', sa.String(), nullable=True))
    op.add_column('stations', sa.Column('type', sa.String(), nullable=False, server_default=StationType.TRANSMISSION.value))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
