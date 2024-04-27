"""Create plan table

Revision ID: a1b295e75aed
Revises: 
Create Date: 2024-02-28 08:20:18.876096

"""
from datetime import datetime
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b295e75aed'
down_revision: Union[str, None] = '2a912db6d9ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'indicators',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )

    op.create_table(
        'training_plan',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(200)),
        sa.Column('description', sa.String(200)),
        sa.Column('duration', sa.Integer()),
        sa.Column('sport', sa.Integer()),
        sa.Column('intensity', sa.String(20)),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )

    op.create_table(
        'training_plan_sportman',
        sa.Column('id', sa.String(36), primary_key=True, index=True, nullable=False, unique=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('time', sa.String(50), nullable=True),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('sportsman_id', sa.Integer, sa.ForeignKey('sportsman.id'), nullable=False),
        sa.Column('training_plan_id', sa.Integer, sa.ForeignKey('indicators.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )

    op.create_table(
        'monitoring',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('session_id', sa.String(36), sa.ForeignKey('training_plan_sportman.id'), nullable=False),
        sa.Column('indicators_id', sa.Integer, sa.ForeignKey('indicators.id'), nullable=False),
        sa.Column('value', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('monitoring')
    op.drop_table('training_plan')
    op.drop_table('indicators')
    op.drop_table('sports_session')
