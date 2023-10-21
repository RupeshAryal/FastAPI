"""create vote tables

Revision ID: 64c3b6b4d5bb
Revises: 7ca9b811063e
Create Date: 2023-10-21 14:13:24.044707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64c3b6b4d5bb'
down_revision: Union[str, None] = '7ca9b811063e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("votes",
                    sa.Column("post_id", sa.Integer(), primary_key=True, nullable=False),
                            sa.Column("user_id", sa.Integer(), primary_key=True, nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table("votes")
    pass
