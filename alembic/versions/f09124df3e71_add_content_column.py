"""add content column

Revision ID: f09124df3e71
Revises: d7071e45411b
Create Date: 2023-10-20 19:59:33.702532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f09124df3e71'
down_revision: Union[str, None] = 'd7071e45411b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('content', sa.Text(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
