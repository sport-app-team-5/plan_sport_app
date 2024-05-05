"""fix type data

Revision ID: 04344edac18a
Revises: 3dd36489a973
Create Date: 2024-05-03 12:32:17.332822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04344edac18a'
down_revision: Union[str, None] = '3dd36489a973'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('training_plan', 'sport',  type_=sa.String(100))


def downgrade() -> None:
    op.alter_column('training_plan', 'sport',  type_=sa.Integer)
