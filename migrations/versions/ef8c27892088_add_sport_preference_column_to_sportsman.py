"""add sport_preference column to sportsman

Revision ID: ef8c27892088
Revises: 7381846ab0a0
Create Date: 2024-04-22 11:28:27.202375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef8c27892088'
down_revision: Union[str, None] = '7381846ab0a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('sportsman', sa.Column('sport_preference', sa.String(length=200), nullable=True))


def downgrade() -> None:
    op.drop_column('sportsman', 'sport_preference')
