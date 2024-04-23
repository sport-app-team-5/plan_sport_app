"""empty message

Revision ID: 7381846ab0a0
Revises: 4997d25c3629, a1b295e75aed, c0ff0624f01e
Create Date: 2024-04-22 11:28:09.472683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7381846ab0a0'
down_revision: Union[str, None] = ('4997d25c3629', 'a1b295e75aed', 'c0ff0624f01e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
