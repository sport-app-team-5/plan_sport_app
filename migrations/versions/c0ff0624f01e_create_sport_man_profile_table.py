"""Create sport man profile table

Revision ID: c0ff0624f01e
Revises: 2a912db6d9ec
Create Date: 2024-04-21 09:48:49.651015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0ff0624f01e'
down_revision: Union[str, None] = '2a912db6d9ec'
branch_labels: Union[str, Sequence[str], None] = ('sport_man_profile',)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'injuries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.String(200), nullable=False),
        sa.Column('severity', sa.Integer, nullable=False),        
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )

    op.create_table(
        'sportman_injury',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('id_sporman', sa.Integer, sa.ForeignKey('sportsman.id')),
        sa.Column('id_injury', sa.Integer, sa.ForeignKey('injuries.id')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    


def downgrade() -> None:
    op.drop_table('allergy_sportman')
    op.drop_table('allergy')
