"""add published column and created at column

Revision ID: 7ca9b811063e
Revises: 06673db1adf3
Create Date: 2023-10-21 14:00:39.392558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ca9b811063e'
down_revision: Union[str, None] = '06673db1adf3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("published", sa.Boolean, server_default=sa.text('TRUE'),nullable=False))

    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "posts")
    pass

