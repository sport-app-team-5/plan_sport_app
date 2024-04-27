"""empty message

Revision ID: b27e30eecf92
Revises: 4997d25c3629, a1b295e75aed, ef8c27892088
Create Date: 2024-04-23 20:05:48.352488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b27e30eecf92'
down_revision: Union[str, None] = ('4997d25c3629', 'a1b295e75aed', 'ef8c27892088')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
