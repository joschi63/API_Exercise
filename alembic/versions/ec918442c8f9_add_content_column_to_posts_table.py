"""add content column to posts table

Revision ID: ec918442c8f9
Revises: b91a25d8216b
Create Date: 2025-10-12 12:25:56.238144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec918442c8f9'
down_revision: Union[str, None] = 'b91a25d8216b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
