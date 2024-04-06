"""Add subscription table

Revision ID: 4eab20af7d4b
Revises: 2a912db6d9ec
Create Date: 2024-04-06 09:16:25.638607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.modules.sport_man.domain.enum.subscription_type_enum import SubscriptionType


# revision identifiers, used by Alembic.
revision: str = '4eab20af7d4b'
down_revision: Union[str, None] = 'a1b295e75aed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'subscription',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('description', sa.String(length=200), nullable=True),
        sa.Column('type',  sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )


def downgrade():
    op.drop_table('subscription')