"""add exercise_experience and time_dedication_sport column to sportsman

Revision ID: a6260c9daf28
Revises: b27e30eecf92
Create Date: 2024-04-23 20:05:57.967911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6260c9daf28'
down_revision: Union[str, None] = 'b27e30eecf92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('sportsman', sa.Column('exercise_experience', sa.String(length=200), nullable=True))
    op.add_column('sportsman', sa.Column('time_dedication_sport', sa.String(length=200), nullable=True))


def downgrade() -> None:
    op.drop_column('sportsman', 'exercise_experience')
    op.drop_column('sportsman', 'time_dedication_sport')

