"""add last few columns to posts table

Revision ID: 9ffd7bbf6547
Revises: 0216cca69132
Create Date: 2025-10-12 12:53:02.144524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ffd7bbf6547'
down_revision: Union[str, None] = '0216cca69132'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean, server_default='TRUE', nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False))
    op.add_column('posts', sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=None, onupdate=sa.text("now()"), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'updated_at')
    pass
