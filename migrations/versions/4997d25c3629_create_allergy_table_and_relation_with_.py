"""create allergy table and relation with Sportsman table

Revision ID: 4997d25c3629
Revises: 2a912db6d9ec
Create Date: 2024-04-09 21:25:05.125168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4997d25c3629'
down_revision: Union[str, None] = '2a912db6d9ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'allergy',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.String(200), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )
    op.create_table(
        'allergy_sportman',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('sportsman_id', sa.Integer(), sa.ForeignKey('sportsman.id')),
        sa.Column('allergy_id', sa.Integer(), sa.ForeignKey('allergy.id')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),

    )


def downgrade() -> None:
    op.drop_table('allergy_sportman')
    op.drop_table('allergy')

