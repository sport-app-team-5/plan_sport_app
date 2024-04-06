"""Add sportman table

Revision ID: 2a912db6d9ec
Revises: a1b295e75aed
Create Date: 2024-04-06 09:15:38.668310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.modules.sport_man.domain.enum.food_preference_enum import FoodPreference
from app.modules.sport_man.domain.enum.trining_goal_enum import TrainingGoal


# revision identifiers, used by Alembic.
revision: str = '2a912db6d9ec'
down_revision: Union[str, None] = 'ab260bd17a76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'sportsman',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('sport_profile_id', sa.Integer(), sa.ForeignKey('sport_profile.id'), nullable=True),
        sa.Column('subscription_id', sa.Integer(), sa.ForeignKey('subscription.id'), nullable=True),
        sa.Column('food_preference', sa.String(20), nullable=True),
        sa.Column('training_goal', sa.String(20), nullable=True),
        sa.Column('birth_year', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('weight', sa.Integer(), nullable=True),
        sa.Column('body_mass_index', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )


def downgrade():
    op.drop_table('sportsman')