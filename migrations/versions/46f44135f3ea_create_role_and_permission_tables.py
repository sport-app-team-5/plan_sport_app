"""Create role and permission tables

Revision ID: 46f44135f3ea
Revises: a1b295e75aed
Create Date: 2024-02-28 17:12:55.389779

"""
from datetime import datetime
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b295e75aed'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('code', sa.CHAR(4), nullable=False, unique=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )
    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('code', sa.String(5), unique=True, nullable=False),
        sa.Column('name', sa.String(100), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )
    op.create_table(
        'permission_roles',
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'), primary_key=True, index=True),
        sa.Column('permission_id', sa.Integer(), sa.ForeignKey('permissions.id'), primary_key=True, index=True),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('role_permission')
    op.drop_table('permissions')
    op.drop_table('roles')
