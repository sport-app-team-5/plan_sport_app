"""add is_inside_house in training_plan table

Revision ID: 20c168d7d5fc
Revises: 04344edac18a
Create Date: 2024-05-07 09:54:36.354598

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20c168d7d5fc'
down_revision: Union[str, None] = '04344edac18a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('training_plan', sa.Column('is_inside_house', sa.Boolean, nullable=False))


def downgrade() -> None:
    op.drop_column('training_plan', 'is_inside_house')
