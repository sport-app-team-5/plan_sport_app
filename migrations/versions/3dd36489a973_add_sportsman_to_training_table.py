"""Add sportsman to training table

Revision ID: 3dd36489a973
Revises: 73dfcde1e6e4, a6260c9daf28
Create Date: 2024-05-03 08:07:12.370288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dd36489a973'
down_revision: Union[str, None] = ('73dfcde1e6e4', 'a6260c9daf28')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('training_plan', sa.Column('sportsman_id', sa.Integer(), sa.ForeignKey('sportsman.id'), index=True))


def downgrade() -> None:
    op.drop_column('training_plan', 'sportsman_id')
