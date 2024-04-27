"""add risk column to sportsman

Revision ID: 73dfcde1e6e4
Revises: a6260c9daf28
Create Date: 2024-04-26 16:43:44.924068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73dfcde1e6e4'
down_revision: Union[str, None] = 'ef8c27892088'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('sportsman', sa.Column('risk', sa.String(length=200), nullable=True))


def downgrade() -> None:
    op.drop_column('sportsman', 'risk')
