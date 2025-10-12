"""create posts table

Revision ID: b91a25d8216b
Revises: 
Create Date: 2025-10-12 11:34:49.043988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b91a25d8216b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String, nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
