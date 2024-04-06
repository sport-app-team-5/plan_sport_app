"""Add sport profile table

Revision ID: ab260bd17a76
Revises: 4eab20af7d4b
Create Date: 2024-04-06 09:16:54.159199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab260bd17a76'
down_revision: Union[str, None] = '4eab20af7d4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'sport_profile',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('ftp', sa.String(length=5), nullable=True),
        sa.Column('vo2_max', sa.String(length=5), nullable=True),
        sa.Column('training_time', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )


def downgrade():
    op.drop_table('sport_profile')