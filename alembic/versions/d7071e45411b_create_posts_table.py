"""create posts table

Revision ID: d7071e45411b
Revises: 
Create Date: 2023-10-20 19:37:30.048388

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd7071e45411b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(2000), nullable=False))



def downgrade() -> None:
    op.drop_table('posts')
